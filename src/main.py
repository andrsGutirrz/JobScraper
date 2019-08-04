
import argparse
import scraping_web as scrap


parser = argparse.ArgumentParser(description='Web Scraper')
parser.add_argument('--name', type=str, required=True, help='Output CSV name')
args = parser.parse_args()


if __name__ == "__main__":
    scrap.toCSV(args.name)
