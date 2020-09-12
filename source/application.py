from flask import Flask, render_template, url_for, escape
from flask_flatpages import FlatPages
import os
from PIL import Image
from resizeimage import resizeimage

CWD = os.path.dirname(os.path.realpath(__file__))
FORCE_RESIZE = False

application = Flask(__name__)
application.config["FREEZER_BASE_URL"] = "http://properveganfood.com/"
application.config["FLATPAGES_EXTENSION"] = ".md"

pages = FlatPages(application)

@application.route('/index.html')
@application.route('/')
def index():
    latest = sorted(pages, reverse=True, key=lambda p: p.meta['published'])
    return render_template('index.html', recipes = latest[:10])

@application.route('/recipes/')
def recipes():
    latest = sorted(pages, reverse=True, key=lambda p: p.meta['published'])
    return render_template('recipes.html', recipes = latest, title = "Recipes")


@application.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    folder = path.split('/')[0].lower()
    if folder == "recipes":
        title = page.meta.get("title", None) + " Recipe"
        return render_template('recipe.html', recipe=page, title=title)


@application.template_filter('resize')
def resize(img_path, width: int, height: int):
    img_path = img_path[1:]
    path, filename = os.path.split(img_path)
    new_path = os.path.join(path, "resized", f"w{width}_h{height}_{filename}")
    if FORCE_RESIZE or not os.path.exists(new_path):
        img = Image.open(img_path)
        img = resizeimage.resize_cover(img, (width, height))
        img.save(new_path, img.format)
    return f"/{new_path}"

@application.template_filter('resize_width')
def resize_width(img_path, width: int):
    img_path = img_path[1:]
    path, filename = os.path.split(img_path)
    new_path = os.path.join(path, "resized", f"w{width}_{filename}")
    if FORCE_RESIZE or not os.path.exists(new_path):
        img = Image.open(img_path)
        img = resizeimage.resize_width(img, width)
        img.save(new_path, img.format)
    return f"/{new_path}"


if __name__ == "__main__":
    application.run(debug=True)
