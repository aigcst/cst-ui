import cst_ui as ui

app = ui.App()


@app.page("/", title="Home")
def test(data: ui.DataAdmin):
    # page = data.page
    # cstos.set_theme(page)
    return ui.View(
        controls=[ui.Text("Hello World")],
    )


if __name__ == "__main__":
    app.run()
    # cstos.app(main)
