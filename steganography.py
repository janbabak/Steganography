import argparse
import logging.config
from service.EmbedService import EmbedService

# logging set up
logging.config.fileConfig('logger.conf')
pil_logger = logging.getLogger('PIL')
pil_logger.setLevel(logging.INFO)

embedService = EmbedService.get_instance()

# argument parser
parser = argparse.ArgumentParser(description="Steganography")
parser.add_argument('-e', '--embed', action='store_true', help='Embed data to input image.')
parser.add_argument('-x', '--extract', action='store_true', help='Extract data from input image.')
parser.add_argument('-p', '--password', type=str, help='Secret password for encryption and decryption.')
parser.add_argument('-i', '--input-file', type=str, help='File to embed data into or extract data from.')
parser.add_argument('-f', '--file-content', type=str, help='File content to embed.')
parser.add_argument('-s', '--string-content', type=str, help='String to embed into the input image.')
parser.add_argument('-o', '--output-file', type=str, help='Output file that will contain the embedded file ' + 
                    'in case of embedding, extracted data in case of extracting')

args = parser.parse_args()

if args.embed:
    if args.string_content:
        print(f'string content is: {args.string_content}')
        embedService.embed_string(args.string_content, args.input_file, args.output_file, args.password)
    elif args.file_content:
        embedService.embed_file(args.file_content, args.input_file, args.output_file, args.password)
elif args.extract:
    embedService.get_embedded_message(args.input_file, args.output_file, args.password)
