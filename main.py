from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

from calculator import calculate


class CalculatorLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.display = TextInput(
            hint_text="Enter expression (e.g. 2+3*5)",
            multiline=False,
            font_size=24
        )
        self.add_widget(self.display)

        self.result = Label(
            text="Result",
            font_size=22
        )
        self.add_widget(self.result)

        btn = Button(
            text="Calculate",
            size_hint=(1, 0.2)
        )
        btn.bind(on_press=self.solve)
        self.add_widget(btn)

    def solve(self, instance):
        try:
            answer = calculate(self.display.text)
            self.result.text = str(answer)
        except Exception as e:
            self.result.text = f"Error: {e}"


class CalculatorKMS(App):
    def build(self):
        return CalculatorLayout()


if __name__ == "__main__":
    CalculatorKMS().run()
