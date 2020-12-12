
class HTML_Generator:
    # Usage example:
    '''
    html = HTML_Generator(outfile = "output.html", name="my_ranked_doc.txt")
    html.add_text("text to always show, of the ranked document")
    html.add_match(match_name, match_score, match_text)
    html.write_file()
    '''

    def __init__(self, outfile, name):
        self.outfile = outfile
        self.name = name
        self.outstr = '''
            <!-- source: W3 Schools https://www.w3schools.com/howto/howto_js_collapsible.asp -->
            <!DOCTYPE html>
            <html>
            <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
            .collapsible {
              background-color: #777;
              color: white;
              cursor: pointer;
              padding: 18px;
              width: 100%;
              border: none;
              text-align: left;
              outline: none;
              font-size: 15px;
            }

            .active, .collapsible:hover {
              background-color: #555;
            }

            .collapsible:after {
              content: '\002B';
              color: white;
              font-weight: bold;
              float: right;
              margin-left: 5px;
            }

            .active:after {
              content: "\2212";
            }

            .content {
              padding: 0 18px;
              max-height: 0;
              overflow: hidden;
              transition: max-height 0.2s ease-out;
              background-color: #f1f1f1;
            }
            </style>
            </head>
            <body>
            '''
        self.outstr += "<h2>Rank for: " + self.name + "</h2>"

    def add_divide(self, text):
        self.outstr += "<hr/><hr/><hr/><h1>" + str(text) + "</h1>"

    def add_title(self, text):
        self.outstr += "<h3>" + str(text) + "</h3>"

    def add_text(self, text):
        self.outstr += "<p>" + str(text) + "</p>"

    def add_match(self, match_name, match_score, match_text):
        self.outstr += "<button class=\"collapsible\"> similarity found: " + str(match_name) + "(score=" + str(match_score) + ") " + "</button>"
        self.outstr += "<div class=\"content\"><p>" + str(match_text) + "</p></div>"

    def write_file(self):
        self.outstr += '''
            <script>
            var coll = document.getElementsByClassName("collapsible");
            var i;

            for (i = 0; i < coll.length; i++) {
              coll[i].addEventListener("click", function() {
                this.classList.toggle("active");
                var content = this.nextElementSibling;
                if (content.style.maxHeight){
                  content.style.maxHeight = null;
                } else {
                  content.style.maxHeight = content.scrollHeight + "px";
                } 
              });
            }
            </script>

            </body>
            </html>
            '''

        # print(self.outstr)

        f = open(self.outfile, "w")
        f.write(self.outstr)
        f.close()

        print("\nDropping your pen and rubbing your temples, you look over", self.outfile, "and smile knowing the analysis is done.  ")




