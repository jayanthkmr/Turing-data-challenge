# Turing-data-challenge

There are two ways to run the script. Both require AWS EC2 instance set up.

## AWS Set up

Launch an AWS EC2 instance and ssh into it. Run the following commands to set it up:

```bash
sudo yum update
sudo yum install git
git clone https://github.com/jayanthjaiswal/Turing-data-challenge.git
sudo pip install tqdm mrjob wget
```

Above I have used git to clone the repository, you can use scp to copy the files too:

```bash
scp -i key.pem Turing-data-challenge ec2-user@x.x.xx.xx:Turing-data-challenge
```

## Running it locally with threads

This takes around a day (~24 hrs) to complete and outputs the result in result.json.

```bash
# Directly running it on multiprocessor
cd Turing-data-challenge
chmod +x pycodemetrics/src/eval.py
nohup pycodemetrics/src/eval.py pycodemetrics/url_list.csv &
```

To check the status of the running code, look into nohup.out.
```bash
tail nohup.out
```

To copy the results back after 24 hrs, use scp:

```bash
scp -i key.pem ec2-user@x.x.xx.xx:Turing-data-challenge/results.json results.json
```

## Running it on EMR

This takes around ~6hrs to complete but outputs the result on stdout(nohup.out), which later requires
manual cleaning. But before running the code, you need to set up the file .mrjobconf with your AWS key 
and AWS secret key.

```yaml
# .mrjobconf file
runners:
  emr:
    aws_access_key_id: UR_AWS_KEY
    aws_secret_access_key: UR_AWS_SECRET_KEY
    setup:
    - VENV=/tmp/$mapreduce_job_id
    - if [ ! -e $VENV ]; then virtualenv $VENV; fi
    - . $VENV/bin/activate
    - pip install tqdm mrjob wget
```
To access your access key id and secret access key, follow this [link](https://help.bittitan.com/hc/en-us/articles/115008255268-How-do-I-find-my-AWS-Access-Key-and-Secret-Access-Key-).

After updating mrjob conf file with your key, log into AWS instance and run the mrjob code:

```bash
# Directly running it on EMR
cd Turing-data-challenge
chmod +x pycodemetrics/src/mrjobeval.py
nohup pycodemetrics/src/mrjobeval.py pycodemetrics/url_list.csv -r emr &
```

To check the status of the running code, look into nohup.out.
```bash
tail nohup.out
```

To copy the results back after 6 hrs, use scp:

```bash
scp -i key.pem ec2-user@x.x.xx.xx:Turing-data-challenge/nohup.out nohup.out
```

Finally, open the nohup.out and delete the lines corresponding to logs.
