from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

outfits = []


@app.route("/")
def outfit_creator():
    return render_template("outfitcreator.html")


@app.route('/outfitgallery')
def outfit_gallery():
    return render_template("outfitgallery.html", outfits=outfits)


@app.route("/save_outfit", methods=["POST"])
def save_outfit():
    top_image = request.form["top_image"]
    top_color = request.form["top_color"]
    bottom_color = request.form["bottom_color"]
    outer_color = request.form["outer_color"]
    shoe_color = request.form["shoe_color"]
    acc_color = request.form["acc_color"]
    outfit_name = request.form.get("outfit_name", "Unnamed Outfit")

    # Save the outfit details in a database or a file (this is a placeholder)
    new_outfit = {
        "top_image": top_image,
        "top_color": top_color,
        "bottom_color": bottom_color,
        "outer_color": outer_color,
        "shoe_color": shoe_color,
        "acc_color": acc_color,
        "outfit_name": outfit_name,
    }

    outfits.append(
        new_outfit
    )  # Assuming 'outfits' is a global list or loaded from a database/file

    return redirect(url_for("outfit_gallery"))


if __name__ == "__main__":
    app.run(debug=True)
