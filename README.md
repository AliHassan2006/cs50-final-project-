# cs50-final-project-
Today, December 5, 2025, I'm presenting my final project: a letter-to-number converter. This application solves a simple yet useful problem: converting English letters to numbers and vice versa. Many of us sometimes need to convert letters to numbers for cryptography or gaming purposes.

The idea is simple: A becomes 1, B becomes 2, and so on until Z becomes 26. But instead of doing it manually, I built a complete web application that performs this conversion quickly and accurately.

Let's see how the application works:
First: Two-way conversion – from text to numbers and from numbers to text.

Second: Choosing the appropriate separator – you can use a slash, dash, period, pipe, or even a space.

Third: Additional features such as copying to the clipboard, voice pronunciation, and saving results.

Fourth: History Tracking - Each conversion is saved with the time and date.

Let's try the app:
Enter HELLO → Result: 8/5/12/12/15
Now reverse: Enter 1/2/3/4/5 → Result: ABCDE
Try changing the separator to a dash: HELLO becomes 8-5-12-12-15
Try the pronunciation feature: The app will pronounce the result for you
And look at the history page: All previous conversions are stored and organized.
I built this app using Python with the Flask framework for the backend, and JavaScript and HTML/CSS for the frontend.
The database is SQLite, which stores all conversions.
The app is responsive and works on all devices, from computers to phones.
https://github.com/AllHassan2006/cs50-final-project
MIT License
