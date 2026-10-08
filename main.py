import sys
from pathlib import Path

from PyQt6 import QtWidgets, uic


def create_window() -> QtWidgets.QMainWindow:
    ui_path = Path(__file__).with_name("vit.ui")
    window: QtWidgets.QMainWindow = uic.loadUi(str(ui_path))
    page_stack = window.findChild(QtWidgets.QStackedWidget, "pageStack")
    candidate_name_input = window.findChild(QtWidgets.QLineEdit, "candidateNameInput")
    candidate_email_input = window.findChild(QtWidgets.QLineEdit, "candidateEmailInput")
    candidate_course_input = window.findChild(QtWidgets.QComboBox, "candidateCourseInput")
    candidate_add_button = window.findChild(QtWidgets.QPushButton, "candidateAddButton")
    candidates_table = window.findChild(QtWidgets.QTableWidget, "candidatesTable")
    candidate_count = window.findChild(QtWidgets.QLabel, "candidateMetricValue")
    schedule_candidate_input = window.findChild(QtWidgets.QComboBox, "scheduleCandidateInput")
    schedule_round_input = window.findChild(QtWidgets.QComboBox, "scheduleRoundInput")
    schedule_date_input = window.findChild(QtWidgets.QDateEdit, "scheduleDateInput")
    schedule_time_input = window.findChild(QtWidgets.QTimeEdit, "scheduleTimeInput")
    schedule_staff_input = window.findChild(QtWidgets.QComboBox, "scheduleStaffInput")
    schedule_add_button = window.findChild(QtWidgets.QPushButton, "scheduleAddButton")
    schedule_table = window.findChild(QtWidgets.QTableWidget, "scheduleTable")
    upcoming_table = window.findChild(QtWidgets.QTableWidget, "upcomingTable")
    interview_count = window.findChild(QtWidgets.QLabel, "interviewMetricValue")

    navigation = (
        ("navDashboard", 0),
        ("navSchedule", 1),
        ("navCandidates", 2),
        ("navResults", 3),
    )
    required_widgets = (
        page_stack,
        candidate_name_input,
        candidate_email_input,
        candidate_course_input,
        candidate_add_button,
        candidates_table,
        candidate_count,
        schedule_candidate_input,
        schedule_round_input,
        schedule_date_input,
        schedule_time_input,
        schedule_staff_input,
        schedule_add_button,
        schedule_table,
        upcoming_table,
        interview_count,
    )
    if any(widget is None for widget in required_widgets):
        raise RuntimeError("Arayüzde gerekli form veya tablo bileşenleri bulunamadı.")
    if page_stack is None:
        raise RuntimeError("Arayüzde sayfa alanı bulunamadı.")

    buttons: list[tuple[QtWidgets.QPushButton, int]] = []
    for object_name, index in navigation:
        button = window.findChild(QtWidgets.QPushButton, object_name)
        if button is None:
            raise RuntimeError(f"Arayüzde gezinme düğmesi bulunamadı: {object_name}")
        buttons.append((button, index))

    def show_page(index: int) -> None:
        page_stack.setCurrentIndex(index)
        for button, page_index in buttons:
            button.setChecked(page_index == index)

    for button, index in buttons:
        button.clicked.connect(
            lambda _checked=False, page=index: show_page(page)
        )

    def add_candidate() -> None:
        name = candidate_name_input.text().strip()
        email = candidate_email_input.text().strip()
        if not name or "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            window.statusBar().showMessage(
                "Lütfen adayın adını ve geçerli bir e-posta adresini girin.", 5000
            )
            return

        row = candidates_table.rowCount()
        candidates_table.insertRow(row)
        values = (
            name,
            email,
            candidate_course_input.currentText(),
            "Yeni aday",
            "Planlanmadı",
        )
        for column, value in enumerate(values):
            candidates_table.setItem(row, column, QtWidgets.QTableWidgetItem(value))
        schedule_candidate_input.addItem(name)
        schedule_candidate_input.setCurrentIndex(schedule_candidate_input.count() - 1)
        candidate_count.setText(str(int(candidate_count.text()) + 1))
        candidate_name_input.clear()
        candidate_email_input.clear()
        window.statusBar().showMessage(
            f"{name} aday listesine eklendi (yalnızca bu oturumda).", 5000
        )

    def add_schedule() -> None:
        candidate = schedule_candidate_input.currentText()
        interview_round = schedule_round_input.currentText()
        date = schedule_date_input.date().toString("dd.MM.yyyy")
        time = schedule_time_input.time().toString("HH:mm")
        staff = schedule_staff_input.currentText()

        row = schedule_table.rowCount()
        schedule_table.insertRow(row)
        for column, value in enumerate((candidate, interview_round, date, time, staff)):
            schedule_table.setItem(row, column, QtWidgets.QTableWidgetItem(value))

        upcoming_row = upcoming_table.rowCount()
        upcoming_table.insertRow(upcoming_row)
        for column, value in enumerate(
            (candidate, interview_round, f"{date} • {time}", staff)
        ):
            upcoming_table.setItem(
                upcoming_row, column, QtWidgets.QTableWidgetItem(value)
            )

        interview_count.setText(str(int(interview_count.text()) + 1))
        window.statusBar().showMessage(
            f"{candidate} için görüşme planlandı (yalnızca bu oturumda).", 5000
        )

    candidate_add_button.clicked.connect(add_candidate)
    schedule_add_button.clicked.connect(add_schedule)
    window.statusBar().showMessage("Demo arayüzü • Veriler kalıcı olarak kaydedilmez.")

    return window


def main() -> int:
    app = QtWidgets.QApplication(sys.argv)
    window = create_window()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())