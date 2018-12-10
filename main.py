import reader
import single_run

if __name__ == "__main__":
    filename = "data/test.json"
    parsed_json = reader.read_file(filename)
    singleRun = single_run.SingleRun()
    singleRun.load_json(parsed_json)

    print singleRun.type
    print singleRun.date
    print singleRun.time
    print singleRun.length
