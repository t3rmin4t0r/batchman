The BATCHMAN will save us
=========================

Hadoop clusters are expensive. They need taking care of, funding and occasionally debugging.

But I had a big-data problem, no funding and even more importantly no ops staff.

I needed to crawl approximately 2 Tb of log files every day spread across 600 web nodes and everytime I was looking for something different. And I always needed results immediately.

There were some things which were going my way, thankfully. 

We were at Zynga, but since both me & Binu were from yahoo, we had our log files were formatted with a traditional [yapache format](http://www.radwin.org/michael/talks/yapache-apachecon2005.pdf).

And we were the third and fourth phones to ring when a game was down or misbehaving.

In the original implementation, there was a python orchestrator which ran a fairly complex AWK script on hundreds of nodes, collected all the CSV outputs from them & printed out an aggregate report in seconds.

I've lost the original code I wrote for this, but I found some time to re-do it with an extra bit of crazy. 

AWK is okay for text data, but implementing it all in python looks like a better idea. But I wanted to send bytecode across the wire instead of plain-text python files.

This meant that you could use all kinds of modules available in python, read stuff off sqlite or parse binary files.

Though if I had been working in dev-ops again, I would've zipped up a dir, sent it across, unzipped and ran a command instead of messing with python bytecode. 

But this was never about practicalities was it?

To test this, make sure you have `ssh -v localhost` working with your ssh-agent (without passwords).

Check your keys loaded with `ssh-agent -l` and run `python batchman.py ips` which should print something useless like the file listing of /var/log/ and the python executable path.
