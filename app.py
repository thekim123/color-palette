from flask import Flask, render_template, request
from dotenv import dotenv_values
import openai
import json

config = dotenv_values('.env')
openai.api_key = config["OPENAI_API_KEY"]

app = Flask(__name__, 
    template_folder='templates',
    static_folder='static',
    static_url_path=''
)

@app.route("/")
def index():
    return render_template("index.html")




@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    app.logger.info("HIT THE POST REQUEST ROUTE!!")
    query = request.form.get("query")
    colors = get_colors(query)
    app.logger.info(colors)
    return {"colors": colors}
    # OPEN AI COMPLETION CALL


if __name__ == "__main__":
    app.run(debug=True)



def get_colors(msg):
  prompt = f"""
  You are a color palette generating assistant that responds to text prompts for color palettes.
  You should generate color palettes that fit the theme, mood, or instructions in the prompt.
  The palettes should be between 2 and 8 colors.

  Q: Convert the following verbal description of a color palette into a list of colors: The Mediterranean Sea
  A: ["#006699","#66CCCC","#F0E68C","#008000","#F08080"]

  Q: Convert the following verbal description of a color palette into a list of colors: sage, nature, earth
  A: ["#EDF1D6","#9DC08B","#609966","#40513B"]

  Desired Format: a JSON array of hexadecimal color codes

  Q: Convert the following verbal description of a color palette into a list of colors: {msg}
  A:

  """
 

  response = openai.Completion.create(
      model="gpt-3.5-turbo-instruct",
      prompt=prompt,
      max_tokens=200,
  )

  colorList = response["choices"][0]["text"]
  colors = json.loads(colorList)
  return colors
