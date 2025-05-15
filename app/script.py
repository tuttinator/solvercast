from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import re
import json
from pathlib import Path
import base64
import mimetypes
from glob import glob
from typing import List
from datetime import datetime
import hashlib
import subprocess
import shutil
import random
import requests
from devtools import pprint, PrettyFormat
import docker
from moviepy import VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips
from elevenlabs import ElevenLabs
from dataclasses import dataclass
from pydub import AudioSegment

load_dotenv()

TAG_RE = re.compile(r"^\[S[12]\]")

pp = PrettyFormat()

llm_client = OpenAI()
docker_client = docker.from_env()

ELEVENLABS_MODEL_NAME = "eleven_multilingual_v2"

# Utils


def cache_path(step_idx: str, role: str, text: str, voice_id: str) -> Path:
    h = hashlib.sha256(f"{voice_id}|{text}".encode()).hexdigest()[:16]
    return Path("audio") / f"step_{step_idx}_{role}_{h}.wav"


def image_to_data_url(path: str | Path) -> str:
    path = Path(path).expanduser().resolve()

    mime_type, _ = mimetypes.guess_type(path)
    if mime_type is None:
        mime_type = "application/octet-stream"

    image_bytes = path.read_bytes()

    b64_encoded = base64.b64encode(image_bytes).decode("ascii")

    return f"data:{mime_type};base64,{b64_encoded}"


def parse_turns(raw_script: str) -> list[str]:
    """Return clean speaker-turn strings that always start with [S1] / [S2]."""
    turns, current = [], []
    for line in raw_script.splitlines():
        stripped = line.rstrip()
        if not stripped:  # skip empty lines
            continue
        if TAG_RE.match(stripped):  # new speaker
            if current:
                turns.append(" ".join(current))
            current = [stripped]
        else:  # continuation of previous speaker
            current.append(stripped)
    if current:
        turns.append(" ".join(current))
    return turns


def get_step_idx(path: str) -> int:
    """Extract the numeric index from 'step_<n>.<ext>'."""
    step_pattern = re.compile(r"step_(\d+)\.")
    m = step_pattern.search(Path(path).name)
    return int(m.group(1)) if m else -1


# Pydantic models


class Equations(BaseModel):
    latext: str
    unicode: str


class Prerequisites(BaseModel):
    topic: str
    reason: str


class Givens(BaseModel):
    known_facts: str
    explanation: str


class ProblemAnalysis(BaseModel):
    equations: list[Equations]
    problem_description: str
    prerequisites: list[Prerequisites]
    givens: list[Givens]


class ProblemSolvingStep(BaseModel):
    title: str
    description: str
    hints: str


class Solution(BaseModel):
    steps: list[ProblemSolvingStep]
    final_solution: str


class StepConversation(BaseModel):
    step: str
    script: str


class ConversationScript(BaseModel):
    steps: list[StepConversation]


def main():
    image_dataset = glob("../dataset/images/exam_questions/*.png")

    run_id = str(datetime.now()).replace(" ", "_").replace(":", "_")

    for problem_image in sorted(image_dataset):
        process(problem_image, run_id)


def process_problem_analysis(problem_image: str, log_dir: Path):
    response = llm_client.responses.parse(
        model="o3",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Extract the equations, description of the maths problem, prerequisite required knowledge and known 'givens' in the problem which are helpful in answering the question.",
                    },
                    {
                        "type": "input_image",
                        "image_url": image_to_data_url(problem_image),
                    },
                ],
            }
        ],
        text_format=ProblemAnalysis,
    )
    problem_analysis = response.output_parsed

    with open(log_dir / "problem_analysis.json", "w") as f:
        json.dump(problem_analysis.model_dump(), f)

    return problem_analysis


def process_solving_steps(problem_analysis: ProblemAnalysis, log_dir: Path):
    solving_context = open(
        os.path.dirname(os.path.realpath(__file__)) + "/solving_context.txt", "r"
    ).read()
    solution_step_prompt = f"""Solve this problem step-by-step:

{problem_analysis.problem_description}

The first step should be analysing the problem, identifying the relevant topics necessary to approach this problem and "givens" as part of the question.
{solving_context}

Relevant LaTeX equation:

""" + "\n".join([e.latext for e in problem_analysis.equations])

    problem_response = llm_client.responses.parse(
        model="o3",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": solution_step_prompt},
                ],
            }
        ],
        text_format=Solution,
    )
    solution = problem_response.output_parsed

    with open(log_dir / "solution.json", "w") as f:
        json.dump(solution.model_dump(), f)

    return solution


def generate_manim_script(
    solution: Solution, problem_analysis: ProblemAnalysis, log_dir: Path
):
    manim_prompt = (
        """
You are an expert Manim-CE animator and math instructor.

**Task**
Write a single Python script called **`solve_problem.py`** (Manim CE ≥ 0.18).
The script must define **one Scene class per solution step** so that each scene can be rendered separately:

| Scene class | Corresponds to | Render command example |
|-------------|----------------|------------------------|
"""
        + "\n".join(
            [
                f"| `Step{idx + 1}(Scene) | '{step.title}' | `manim -pqh solve_problem.py Step{idx + 1} -o step_{idx + 1}` |"
                for idx, step in enumerate(solution.steps)
            ]
        )
        + """

**For *each* scene**
1. Use a dark background (`BACKGROUND_COLOR = "#1e1e1e"`).
2. Display the step title in a banner at the top (semi-transparent `BLUE_E`).
3. Show and animate the LaTeX equations with `MathTex`; highlight changes (`YELLOW`, `ORANGE`).
4. Keep ~0.5 s waits between minor animations, ~1 s between major ones.
5. Finish the scene with a short pause (0.5 s) so the last frame isn't cut off.
6. If a visualisation enhances understanding, such as a contour or graph, then include this on the slide.

**Global visual style**
- Text `WHITE`, titles 48 pt, equations 36 pt.
- Use `FadeIn`, `Transform`, `Circumscribe`, and mild `LaggedStart`.
- No audio handling — narration will be added later.

**Input data (do not alter)**

```python
"""
        + pp(problem_analysis)
        + """

"""
        + pp(solution)
        + """
```

Output
Return only the contents of solve_problem.py—no extra comments—so each scene can be rendered like:

```bash
manim -pqh solve_problem.py Step1 -o step_1
manim -pqh solve_problem.py Step2 -o step_2
...
```

Constraints

Wrap repeated UI elements (title banner, highlight routine) in helper functions.

Ensure each scene renders at -pqh quality in ≤ 90 s on a modest laptop.
"""
    )

    manim_script = llm_client.responses.create(
        model="o3",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": manim_prompt},
                ],
            }
        ],
    )

    cleaned_manim_script = "\n".join(
        manim_script.output[1].content[0].text.split("\n")[1:-1]
    )

    with open(log_dir / "solve_problem.py", "w") as f:
        f.write(cleaned_manim_script)

    return cleaned_manim_script


def run_manim_script(manim_script: str, solution: Solution, log_dir: Path):
    host_dir = Path.cwd() / "manim"
    os.makedirs(host_dir, exist_ok=True)
    # Write the manim script to the host directory
    with open(host_dir / "solve_problem.py", "w") as f:
        f.write(manim_script)

    volumes = {
        str(host_dir.resolve()): {
            "bind": "/manim",
            "mode": "rw",
        }
    }
    for idx, _step in enumerate(solution.steps):
        container = docker_client.containers.run(
            image="manimcommunity/manim",
            command=f"manim -pqh solve_problem.py Step{idx + 1} -o step_{idx + 1}",
            working_dir="/manim",
            volumes=volumes,
            tty=True,
            stdin_open=True,
            auto_remove=False,  # Changed to False to allow log capture
            detach=True,
        )

        result = container.wait()
        print("Exit code:", result.get("StatusCode", "unknown"))

        # Capture and save logs
        logs = container.logs().decode("utf-8")
        log_file = log_dir / f"manim_step_{idx + 1}_logs.txt"
        with open(log_file, "w") as f:
            f.write(logs)

        # Remove container after capturing logs
        container.remove()

    return glob("manim/media/videos/solve_problem/1080p60/*.mp4")


def extract_last_frame(video, out_png=None):
    video = Path(video)
    if out_png is None:
        out_png = video.with_suffix(".last.png")

    probe_cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-count_frames",
        "-show_entries",
        "stream=nb_read_frames",
        "-print_format",
        "json",
        str(video),
    ]
    nb_frames = int(
        json.loads(subprocess.check_output(probe_cmd))["streams"][0]["nb_read_frames"]
    )

    select_filter = f"select=eq(n\\,{nb_frames - 1})"
    ff_cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(video),
        "-vf",
        select_filter,
        "-vframes",
        "1",
        str(out_png),
    ]
    subprocess.run(ff_cmd, check=True)
    return Path(out_png)


def generate_script(
    solution: Solution,
    problem_analysis: ProblemAnalysis,
    s1_personality: str,
    s2_personality: str,
    log_dir: Path,
):
    elevenlabs_prompt = (
        r"""
You are designing **dialogue scripts** that will be rendered with the
**ElevenLabs Text-to-Speech API** (multi-voice).
Two distinct voices will be used:

| Tag | Persona | Voice-ID (placeholder) | Personality cues |
|-----|---------|------------------------|------------------|
| `[S1]` | Teacher | `<VOICE_ID_TEACHER>` | """
        + s1_personality
        + """ |
| `[S2]` | Student | `<VOICE_ID_STUDENT>` | """
        + s2_personality
        + """ |

(Our orchestration layer will swap the placeholders for real voice IDs
before calling ElevenLabs.)

───────────────────────────
Conversation specification
───────────────────────────
For **each problem-solving step** in `Solution.steps`, generate a short,
self-contained chat that matches the final slide frame for that step.

1. **Length** 10 – 30 utterances total, focusing on being an engaging conversation to drive understanding and help students learn.
2. **Tone** friendly "chalk & talk"; S1 guides, S2 thinks aloud. Add colour and personality to the conversation with liberal use metaphors.
3. **Slide awareness** Mention what part of the slide the speaker is referring to if it aids in understanding. Do **not** restate the full equation.
4. **Pedagogical arc** S1 → question → S2 reply → S1 confirm/correct → S2 cements understanding → S1 encourages and celebrates → wrap-up.
5. **Pronunciation control** ElevenLabs mispronounces raw math
   symbols; **spell them out**:

   | Symbol | Say … |
   |--------|-------|
   | `x²`   | "x squared" |
   | `/`    | "divided by" |
   | `∫`    | "integral of" |
   | `→`    | "implies" |
   | `ln`   | "natural log" |

   *Never* include LaTeX, superscripts or subscripts directly.
6. **No extra stage directions** beyond the allowed tag.
7. **Order** Do **not** merge steps; output chats in the same order as
   `Solution.steps`.
8. The first interaction on the first slide should introduce the whole problem, give an overview and describe all the prerequisities which are necessary to tackle this problem.
9. The whole conversation should be coherent, engaging and fun. Students watching this video should have more con

──────────────────────────────
Example (abridged, symbol-safe)
──────────────────────────────
Step 2 – Partial Fractions
[S1] Notice the denominator—see "x minus one" times "x plus one"?
[S2] Yes! That means we can split the fraction, right?
[S1] Exactly. What constants should we place on top?
[S2] Let me guess: A over "x minus one" and B over "x plus one."
[S1] Good. Plugging in x equals one gives A equals one-half—keep going!

────────────────────────────────────────────────────────────
**Input data**

```python
"""
        + pp(problem_analysis)
        + """

"""
        + pp(solution)
        + """
"""
    )
    base64_slide_images = [
        {"type": "input_image", "image_url": image_to_data_url(i)}
        for i in glob("manim/media/videos/solve_problem/1080p60/*.last.png")
    ]
    script_collected_prompt = [
        {"type": "input_text", "text": elevenlabs_prompt}
    ] + base64_slide_images

    script_response = llm_client.responses.parse(
        model="o3",
        input=[
            {
                "role": "user",
                "content": script_collected_prompt,
            }
        ],
        text_format=ConversationScript,
    )

    with open(log_dir / "script.json", "w") as f:
        json.dump(script_response.output_parsed.model_dump(), f)

    return script_response.output_parsed


def process_audio_generation(conversation_script: ConversationScript, log_dir: Path):
    elevenlabs_client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

    voice_ids_list = [
        "NOpBlnGInO9m6vDvFkFC",
        "yl2ZDV1MzN4HbQJbMihG",
        "kdmDKE6EkgrWrrykO9Qt",
        "56AoDkrOh6qfVPDXZ7Pt",
        "vfaqCOvlrKi4Zp7C2IAm",
        "KTPVrSVAEUSJRClDzBw7",
        "yjJ45q8TVCrtMhEKurxY",
        "pPdl9cQBQq4p6mRkZy2Z",
        "vBKc2FfBKJfcZNyEt1n6",
        "piI8Kku0DcvcL6TTSeQt",
        "tnSpp4vdxKPjI9w0GnoV",
        "DTKMou8ccj1ZaWGBiotd",
        "flHkNRp1BlvT73UL6gyz",
        "9yzdeviXkFddZ4Oz8Mok",
        "UgBBYS2sOqTuMpoF3BR0",
        "0SpgpJ4D3MpHCiWdyTg3",
        "oR4uRy4fHDUGGISL0Rev",
        "1hlpeD1ydbI2ow0Tt3EW",
        "DtsPFCrhbCbbJkwZsb3d",
        "gOkFV1JMCt0G0n9xmBwV",
    ]

    selected_voices = random.sample(voice_ids_list, 2)

    voice_map = {"[S1]": selected_voices[0], "[S2]": selected_voices[1]}

    with open(log_dir / "voice_map.json", "w") as f:
        f.write(json.dumps(voice_map))

    audio_generation_log = []

    for step_idx, step in enumerate(conversation_script.steps):
        print(f"\n🎬  === Step {step_idx + 1} ===")
        prev_request_ids: list[str] = []

        speaker_turns = parse_turns(step.script)
        speaker_turn_count = len(speaker_turns)
        step_wav_files = []

        for turn_idx, turn in enumerate(speaker_turns):
            role, text = turn[:4], turn[4:].lstrip()
            print(f"Role: {role}")
            print(f"Text: {text}")

            voice_id = voice_map[role]

            wav_path = cache_path(step_idx, role, turn, voice_id)
            if wav_path.exists():
                step_wav_files.append(wav_path)
                print(f"↪︎  cache hit  {wav_path.name}")
                continue

            # prepare context fields
            prev_text = None if turn_idx == 0 else " ".join(speaker_turns[:turn_idx])
            next_text = (
                None
                if turn_idx == speaker_turn_count - 1
                else " ".join(speaker_turns[turn_idx + 1 :])
            )

            # call ElevenLabs via SDK
            audio_bytes = elevenlabs_client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id=ELEVENLABS_MODEL_NAME,
                voice_settings={
                    "speed": 1.2,
                    # "use_speaker_boost": True,
                    "style": 0.5,
                    # "similarity_boost": 0.7,
                    "stability": 0.3,
                },
                # context
                previous_text=prev_text,
                next_text=next_text,
                previous_request_ids=prev_request_ids[-3:],
                # true to see if normalization will also enhance pronunciation
                apply_text_normalization="on",
            )

            with open(wav_path, "wb") as f:
                audio = b"".join(audio_bytes)
                f.write(audio)

            req_id = elevenlabs_client.history.get_all().history[0].request_id
            if req_id:
                prev_request_ids.append(req_id)

            step_wav_files.append(wav_path)
            print(f"✓  {wav_path.name}   req_id={req_id}")
            audio_generation_log.append(
                {
                    "step_idx": step_idx,
                    "turn_idx": turn_idx,
                    "req_id": req_id,
                    "text": text,
                    "voice_id": voice_id,
                }
            )

    with open(log_dir / "audio_generation_log.json", "w") as f:
        json.dump(audio_generation_log, f)

    # combine all step_wav_files files
    # -----------------------------------------------------------
    if step_wav_files:
        combined = AudioSegment.from_file(step_wav_files[0])
        for extra in step_wav_files[1:]:
            combined += AudioSegment.from_file(extra)

        out_slide = Path("audio") / "combined" / f"step_{step_idx + 1}.wav"
        out_slide.parent.mkdir(parents=True, exist_ok=True)
        combined.export(out_slide, format="wav")
        print("🔊  wrote", out_slide.name)


def stitch_audio_and_video(log_dir: Path):
    step_videos_glob = "manim/media/videos/solve_problem/1080p60/step_*.mp4"
    still_image_glob = "manim/media/videos/solve_problem/1080p60/step_*.last.png"
    step_audio_glob = "audio/combined/step_*.wav"
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    videos = {get_step_idx(p): p for p in glob(step_videos_glob)}
    audios = {get_step_idx(p): p for p in glob(step_audio_glob)}
    stills = {get_step_idx(p): p for p in glob(still_image_glob)}

    common_steps = sorted(set(videos) & set(audios) & set(stills))
    if not common_steps:
        raise RuntimeError(
            "No matching step_N.mp4 / step_N.wav / step_N.last.png truple found."
        )

    video_generation_log = []

    for n in common_steps:
        vid_path = videos[n]
        wav_path = audios[n]
        png_path = stills[n]
        out_path = output_dir / f"step_{n:02d}.mp4"

        print(f"[step {n}]  video  → {vid_path}")
        print(f"[step {n}]  audio  → {wav_path}")
        print(f"[step {n}]  still  → {png_path}")

        with (
            VideoFileClip(str(vid_path)) as vclip,
            AudioFileClip(str(wav_path)) as aclip,
        ):
            # ── 1.  Extend video if audio is longer ─────────────────────────
            if aclip.duration > vclip.duration + 1e-3:  # tiny tolerance
                freeze_dur = aclip.duration - vclip.duration

                # still image clip sized exactly like the video
                still_clip = (
                    ImageClip(str(png_path))
                    .with_fps(vclip.fps)
                    .with_duration(freeze_dur)
                )

                vclip = concatenate_videoclips([vclip, still_clip])

            # ── 2.  Add soundtrack and enforce final length ─────────────────
            vclip = vclip.with_audio(aclip).with_duration(aclip.duration)

            # ── 3.  Write final file ────────────────────────────────────────
            vclip.write_videofile(
                str(out_path),
                codec="libx264",
                audio_codec="aac",
                fps=vclip.fps,
                temp_audiofile=str(output_dir / "temp-audio.m4a"),
                remove_temp=True,
                threads=4,
                logger=None,
            )

            video_generation_log.append(
                {
                    "step_idx": n,
                    "video_path": str(out_path),
                    "audio_path": str(wav_path),
                    "still_path": str(png_path),
                }
            )

    with open(log_dir / "video_generation_log.json", "w") as f:
        json.dump(video_generation_log, f)

    print(f"\n✅  All clips rendered to  {output_dir.resolve()}")


def process(problem_image: str, run_id: str):
    print(f"Processing {problem_image} with run_id {run_id}")
    log_dir = Path(f"logs/{os.path.basename(problem_image)}/{run_id}")
    os.makedirs(log_dir, exist_ok=True)

    for folder in ["audio", "output", "manim"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

    # Copy the problem image to the log directory
    shutil.copy(problem_image, log_dir / "problem_image.png")

    print("Processing problem analysis")
    problem_analysis = process_problem_analysis(problem_image, log_dir)
    print("Processing solving steps")
    solution = process_solving_steps(problem_analysis, log_dir)
    print("Generating manim script")
    manim_script = generate_manim_script(solution, problem_analysis, log_dir)
    print("Running manim script")
    video_step_files = run_manim_script(manim_script, solution, log_dir)
    print("Extracting last frames")
    for v in video_step_files:
        png = extract_last_frame(v)
        print("✓", png)

    s1_personality = 'Warm and steady mentor; calm mid-pitch voice, measured pace; frequent gentle affirmations ("great job", "exactly"); uses clear analogies and mild humour to lower anxiety.'
    s2_personality = 'Curious, energetic learner; slightly higher pitch and faster tempo; sprinkles in genuine wonder ("oh, I see!", "that\'s neat"); not afraid to admit confusion, eager to try answers.'

    print("Generating script")
    script = generate_script(
        solution, problem_analysis, s1_personality, s2_personality, log_dir
    )

    print("Processing audio generation")
    process_audio_generation(script, log_dir)
    print("Stitching audio and video")
    stitch_audio_and_video(log_dir)
    print(f"Finished processing {problem_image} with run_id {run_id}")


if __name__ == "__main__":
    main()
