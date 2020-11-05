import sys

from flask import Flask, make_response, render_template, request
from pyvirtualdisplay import Display

sys.path.append("../buhuch")

import pdfkit  # noqa: E402

from hestia.swagger import SalaryTaxCalculatorMixin  # noqa: E402

app = Flask(__name__)
calculator = SalaryTaxCalculatorMixin()


def export_pdf(salary: int):
    display = Display(visible=0, size=(800, 600))
    display.start()

    calculator.salary = salary
    final_salary_value, schema = calculator.find_final_salary(as_dict=True)

    html = render_template(
        "pdf.html", salary=salary, final_salary=final_salary_value, **schema
    )
    pdf = pdfkit.from_string(html, False)
    display.stop()

    response = make_response(pdf)
    response.headers.update(  # type: ignore
        {
            "Content-Type": "application/pdf",
            "Content-Disposition": "inline; filename=output.pdf",
        }
    )
    return response


@app.route("/salary")
def salary_render():
    return render_template("index.html")


@app.route("/pdf_export", methods=["POST"])
def pdf_export():
    return export_pdf(request.get_json()["salary"])


if __name__ == "__main__":
    app.run(debug=True)
