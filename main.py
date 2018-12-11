import reader
import single_run

def load_single_run(filename):
    parsed_json = reader.read_file(filename)
    singleRun = single_run.SingleRun()
    singleRun.load_json(parsed_json)
    return singleRun

if __name__ == "__main__":
    singleRun = load_single_run("data/test.json")

    print singleRun.type
    print singleRun.date
    print singleRun.time
    print singleRun.length
