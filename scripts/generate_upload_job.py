import yaml


def main():
	parser = arguments.setup_parser()
	args = parser.parse_args()
	crawl(args)

if __name__ == '__main__':
    main()