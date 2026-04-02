import json
import gradio as gr

from config import Models
from generator import generate

MODELS = {
    "GPT-5 Nano (OpenAI)":            Models.GPT_5_NANO,
    "GPT-5.4 Mini (OpenAI)":          Models.GPT_5_4_MINI,
    "Claude Haiku 4.5 (Anthropic)":   Models.CLAUDE_HAIKU_4_5,
    "Gemini 2.5 Flash Lite (Google)": Models.GEMINI_2_5_FLASH_LITE,
    "Qwen3 8B (HuggingFace)":         Models.QWEN3_8B,
    "Qwen3 4B (HuggingFace)":         Models.QWEN3_4B,
}


def run_generate(model_name: str, prompt: str, num_records: int):
    if not prompt.strip():
        raise gr.Error("Please enter a prompt.")

    try:
        raw = generate(prompt=prompt, num_records=num_records, model_config=MODELS[model_name])
    except Exception as e:
        raise gr.Error(f"Generation failed: {e}")

    try:
        return json.dumps(json.loads(raw), indent=2), gr.update(visible=True)
    except json.JSONDecodeError:
        return raw, gr.update(visible=True)


def download_json(output: str):
    path = "/tmp/dataset.json"
    with open(path, "w") as f:
        f.write(output)
    return path


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="Synthetic Dataset Generator") as app:
        gr.Markdown("# 🧪 Synthetic Dataset Generator")

        with gr.Row():
            with gr.Column(scale=1):
                model_dropdown = gr.Dropdown(
                    choices=list(MODELS.keys()),
                    value="GPT-5 Nano (OpenAI)",
                    label="Model",
                )
                num_records = gr.Slider(
                    minimum=1, maximum=500, value=20, step=1,
                    label="Number of Records",
                )
                prompt = gr.Textbox(
                    lines=8,
                    placeholder=(
                        "Describe the dataset you want to generate.\n\n"
                        "Example:\n"
                        "Generate customer support tickets with fields:\n"
                        "- ticket_id (string)\n"
                        "- issue (string)\n"
                        "- priority (low | medium | high)\n"
                        "- resolved (boolean)"
                    ),
                    label="Dataset Prompt",
                )
                generate_btn = gr.Button("Generate", variant="primary")

            with gr.Column(scale=1):
                output = gr.Code(
                    label="Output",
                    language="json",
                    interactive=False,
                )
                download_btn = gr.DownloadButton(
                    label="Download JSON",
                    visible=False,
                )

        generate_btn.click(
            fn=run_generate,
            inputs=[model_dropdown, prompt, num_records],
            outputs=[output, download_btn],
        )

        output.change(
            fn=download_json,
            inputs=[output],
            outputs=[download_btn],
        )

    return app


if __name__ == "__main__":
    build_ui().launch()