# Katya: Project Overview

Welcome to the workspace for **Katya**, the AI-driven Alternative Eastern European Student persona.

## 📂 Project Structure

### 1. 🤖 The AI Persona (Chat Bot)
Chat with Katya in real-time to test her personality or generate captions.
*   **Run:** `python src/katya_chat.py`
*   **Config:** Uses `content/planning/system_prompt.txt` and your Google API Key.

### 2. 📸 Visual Assets
Static images and "Ready-to-Post" video slides.
*   **Raw Images:** `content/images/`
*   **TikTok Slides:** `content/ready_to_post/` (Upload these to TikTok in "Photo Mode")
*   **Visual Board:** Open `VISUAL_BOARD.md` to see everything at a glance.

### 3. 📅 Content Strategy
Generate fresh content plans using the AI.
*   **Run:** `python src/generate_content_plan.py`
*   **Output:** Creates a new `WEEKLY_PLAN_YYYY-MM-DD.md` in `content/planning/`.

## 🚀 Quick Start
1.  **Chat with Katya:**
    ```bash
    python src/katya_chat.py
    ```
2.  **Generate New Weekly Plan:**
    ```bash
    python src/generate_content_plan.py
    ```
3.  **Process New Images:**
    (If you add new raw images to `content/images/`)
    ```bash
    python src/process_images.py
    ```

## 📝 Notes
*   **TikTok Strategy:** Use the images in `content/ready_to_post/` as "Photo Carousels". This is a high-converting format for this niche.
*   **Instagram:** Use the `ig_post_*.jpg` images with the "cool tone" filters.
