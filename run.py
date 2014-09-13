from parser_writer import RecordJsonWriter


def handle(input_file_path=None):
    writer = RecordJsonWriter()
    if input_file_path:
        writer.load_input_file(input_file_path)
    else:
        writer.load_input_file('sample-timothy_shaw.in')

    writer.output_json()


if __name__ == "__main__":
    handle()
