from Editing.InferenceWriter import write_inferences
from Scraping.ScrapingEngine import ScrapingEngine

def main():
    se = ScrapingEngine()
    se.run()
    write_inferences(se.getResultSet())

if __name__ == '__main__':
    main()
