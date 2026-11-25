# Can Four Numbers Become One?

Five-minute silent Manim Community animation. The included notebook embeds the full scene. Open Render_Eigenvectors.ipynb in Google Colab, select a Python runtime, set your name and ID in the second code cell, then run all cells. The final cell downloads the 1920 x 1080, 30 fps MP4. A working internet connection is required for the dependency installation. Allow time for rendering.

## Local rendering

Use Python 3.11 or 3.12 with Manim Community 0.19.0 and its system dependencies installed. On Ubuntu/Colab the notebook lists the package prerequisites. No LaTeX is used.

```sh
cd Code
python -m pip install -r requirements.txt
STUDENT_NAME='Your name' STUDENT_ID='Your ID' python -m manim -qh --fps 30 -o Eigenvectors.mp4 eigenvectors.py EigenFilm
```

The file is normally under media/videos/eigenvectors/1080p30/. To preview quickly, change -qh to -ql and --fps 30 to --fps 15. All animation, geometry, text, timing and rendering are implemented through Manim. The PDF and Markdown are supporting documents. No narration or music is included. Add your own narration for the course submission.


# files
the ipynb is the jupyter notebbod used in google coogle collab as normal systems cant render this complex animations

## During the viva

The matrix sends (x,y) to (x+2y,2x+y). Its action is 3 times the identity on the line y=x and minus the identity on y=-x. The intermediate frames use the interpolation (1-t)I+tA. Halfway through, the blue diagonal collapses to the origin before reversing. Eigenpairs describe the final matrix A.

The moving grid and arrows share that interpolation; dashed guides and open input-tip circles stay fixed. In eigenvectors.py, construct sets the cue times, plot computes the geometry, flow animates it, and until holds the last frame for the recording. Set the name and ID before rendering. Update the notebook source cell too if using that route after editing the standalone Python file.

## Credits

Visual reference: https://www.3blue1brown.com/lessons/eigenvalues/

Animation engine: https://www.manim.community/

ChatGPT assisted with the script and animation code.
# eigen-vectors-animation
