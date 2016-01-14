Title: AWS Part 3 : Installing python and custom AMI
Date: 2016-01-04
Series: AWS Tutorials
Category: AWS
Tags: AWS
Author: TDB
Summary: In this tutorial, we will see how to create a scientific workspace (python) on an Amazon instance, and save this configuration for future use.

# 1. Launch an Amazon instance

Launch an Amazon instance corresponding to your needs.
For more information, check [AWS Part 1](../AWS tutorial part 1).


# 2. Install python software

- Once the instance is running, SSH to it as seen in  [AWS Part 1](../AWS tutorial part 1).
- Download Anaconda with wget :

	`wget https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda2-2.4.1-Linux-x86_64.sh`

- Install Anaconda :

	`bash Anaconda2-2.4.1-Linux-x86_64.sh`

- In case you need permission, just append `sudo` to each command
- Accept the conditions and the installation should start.
- When Anaconda asks whether you want to prepend its path to your $PATH variable, type yes.
- Reload your .bashrc

	source .bashrc

If everything worked, you should see the following messages when calling `python`

	Python 2.7.11 |Anaconda 2.4.1 (64-bit)| (default, Dec  6 2015, 18:08:32) 
	[GCC 4.4.7 20120313 (Red Hat 4.4.7-1)] on linux2
	Type "help", "copyright", "credits" or "license" for more information.
	Anaconda is brought to you by Continuum Analytics.
	Please check out: http://continuum.io/thanks and https://anaconda.org

- You can now import classic modules such as numpy, pandas etc.

# 3. Create an AMI for this instance

- In the AWS console, select the instance you just launched
- **Actions** => **Image** => **Create Image**.
- Give a name and a description to your instance, then **Create Image**.
- By default, Amazon will reboot your instance. You can choose not too by ticking the **No Reboot** window.

	The system is going down for reboot NOW!
	Control-Alt-Delete pressed 
	Connection to ec2-52-62-15-17.ap-southeast-2.compute.amazonaws.com closed by remote host.
	Connection to ec2-52-62-15-17.ap-southeast-2.compute.amazonaws.com closed.

- By checking on the **AMI** pane in the console, you should see your image being created.
- You can now launch an instance from your new AMI.
- It contains all the packages that we installed in step 2.