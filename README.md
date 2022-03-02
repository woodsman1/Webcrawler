# WebCrawler and Malicious Url Detection

A simple webcrawler, mainly targeting the link validation and predicting malicious urls. It runs in bfs mode and crawles till user specified depth concurrently and store the details of crawled urls in csv file.

## Features
 - Crawl in BFS mode.
 - Concurrent Running (threads).
 - More than one crawl seeds can be added.
 - generate csv file of crawled urls Status Code and Response Time.
 - Predict if the url is malicious or benign.
 - predicted url can be either benign, defacement, malware or phising.
 - Created a python package using setup.py.

![](/results/crawl.png)

![](/results/predict.png)


## Installation

Clone the repository
```
git clone https://github.com/woodsman1/Webcrawler.git
```

Create a python virtual environment
```
virtualenv venv
```

Install dependencies
```
pip install -r requirements.txt
```

Download Trained models from [here](https://drive.google.com/file/d/1TCwEPexcSwWKj2Lw0dUm_q5QXVmgYpWA/view?usp=sharing) and add it in the model directory.
```
/models/malicious_url.pkl
```

Install Crawler as package
```
python setup.py install
```

## Usage

```text
$ webcrawler -h
usage: webcrawler [-h] [--seeds SEEDS] [--crawl-mode CRAWL_MODE]
                  [--max-depth MAX_DEPTH] [--concurrency CONCURRENCY]
                  [--predict PREDICT]

Crawler sites and extracting links and checking the validity also predict
user specified urls

optional arguments:
  -h, --help            show this help message and exit
  --seeds SEEDS         Seed url(s), if more than one add pipe(|) in
                        betweeen. eg."x.com|y.com|z.com".
  --crawl-mode CRAWL_MODE
                        Add crawling method, bfs or dfs.
  --max-depth MAX_DEPTH
                        Specify max crawl depth.
  --concurrency CONCURRENCY
                        Specify concurrency number.
  --predict PREDICT     Predict if url is malicious or safe. Add url you
                        want to predict its type

```


## Examples

Crawl in BFS mode with 12 concurrent workers, and set maximum depth to 4

```
webcrawler --seeds https://www.google.com/ | https://github.com/woodsman1 -- crawl-mode BFS --concurrency 12 --max-depth 4
```

Predict urls

```
webcrawler --predict http://www.pashminaonline.com/pure-pashminas
```

* Results will be stored in the result folder in the cloned directory

## License

Open source licensed under the MIT license (see LICENSE file for details).