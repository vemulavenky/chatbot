from utlis.gradio_ui import create_gradio_ui
from dotenv import load_dotenv

load_dotenv()
demo = create_gradio_ui()
demo.launch()

