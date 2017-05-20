from Editing.PrettyPrinter import modifyURLToDiscussion
from Editing.WikiWriter import write_picture_after_title

def test_write_image():
    name = "test.jpg"

    upload_file = open(name, "rb")
    upload_contents = upload_file.read()
    upload_file.close()

    urls = modifyURLToDiscussion(set(["http://wikipast.epfl.ch/wikipast/index.php/Secundinus_Aurelianus"]))
    for url in urls:
        write_picture_after_title(upload_contents, name,url)

if __name__ == '__main__':
    test_write_image()
