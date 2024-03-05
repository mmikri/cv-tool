import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.image import Image
from dotenv import load_dotenv

"""
Definition of Kivy application
"""
class CvApp(App):
    def build(self):
        # Set window size
        Window.size = tuple(map(int, os.getenv('WINDOW_SIZE').strip('[]').split(',')))
        return MyBoxLayout()

"""
Custom layout
"""
class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        self.bind(on_parent=self.on_parent)

    def on_parent(self, instance, value):
        if value:
            left_box = self.ids.left_box
            if left_box:
                left_box.bind(on_size=self.update_size_hint_x)

    def update_size_hint_x(self, instance, value):
        left_box = self.ids.left_box
        if left_box:
            left_box.size_hint_x = instance.width / self.width

"""
Top navigation bar
"""
class TopNavBar(BoxLayout):
    pass

"""
Control buttons
"""
class LeftBox(BoxLayout):
    pass

"""
Image display
"""
class CenterBox(BoxLayout):
    pass

"""
Options for preprocessing
"""
class RightBox(BoxLayout):
    def update_label_text(self, button_text):
        self.ids.right_label.text = f"{button_text}"

"""
User button
"""
class MyAppButton(Button):
    def __init__(self, **kwargs):
        super(MyAppButton, self).__init__(**kwargs)
        self.bind(on_release=self.on_button_release)
        self.filters = os.getenv('IMAGE_EXT', '').split()

    # Method called on button click
    def on_button_release(self, instance):
        button_text = self.text
        actions = {
            'Open': self.show_file_chooser,
            'Open Dir': self.open_directory,
            'Next': self.next_action,
            'Prev': self.prev_action,
            'Save Dir': self.save_directory,
            'Save': self.save_action,
        }
        action = actions.get(button_text, self.update_right_label)
        action()

    # Display file chooser
    def show_file_chooser(self):
        file_chooser = FileChooserListView(on_submit=self.on_file_chosen)
        file_chooser.filters = self.filters
        # Create and display popup containing file chooser
        popup = Popup(title="Select File", content=file_chooser, size_hint=(0.8, 0.8))
        popup.open()

    # Callback called on file selection
    def on_file_chosen(self, instance, value, touch):
        app = App.get_running_app()
        center_box = app.root.ids.center_box
        center_box.clear_widgets()

        if isinstance(instance, FileChooserListView) and value:
            file_path = value[0]

            try:
                image_widget = Image(source=file_path)
                center_box.add_widget(image_widget)
            except Exception as e:
                center_box.add_widget(Label(text=f"Error: {str(e)}"))

            parent = instance.parent
            while parent and not isinstance(parent, Popup):
                parent = parent.parent
            if parent:
                parent.dismiss()
        else:
            instance.dismiss()
    
    # To be implemented according to needed functionalities
    def open_directory(self):
        pass

    def next_action(self):
        pass

    def prev_action(self):
        pass

    def save_directory(self):
        pass

    def save_action(self):
        pass

    # Update default label
    def update_right_label(self):
        app = App.get_running_app()
        app.root.ids.right_box.update_label_text(self.text)

if __name__ == '__main__':
    # Load environment variables from .env file
    try:
        load_dotenv()
    except FileNotFoundError:
        print("Could not find the .env file. Environment variables are not loaded.")
    
    # Run the application
    CvApp().run()