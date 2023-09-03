
import sys
from bs4 import BeautifulSoup, Tag, NavigableString
from bs4 import Comment

def remove_attributes_and_comments(inputfile):
    with open(inputfile, 'r') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Removing comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Removing attributes
    for tag in soup.find_all(True):
        if isinstance(tag, Tag) and tag.name != 'a':
            tag.attrs = {}
            if all(isinstance(c, NavigableString) for c in tag.contents) and tag.get_text(strip=True) == '':
                tag.decompose()

    with open('output.html', 'w') as f:
        f.write(str(soup))

# Including the rest of the code for completeness
# usage example
# pass the input file name as argument
if __name__ == "__main__":
    remove_attributes_and_comments(sys.argv[1])
