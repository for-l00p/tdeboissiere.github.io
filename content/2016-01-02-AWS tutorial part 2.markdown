Title: AWS Part 2 : EC2 instances
Date: 2016-01-02
Series: AWS Tutorials
Category: AWS
Tags: AWS
Author: TDB
Summary: In this tutorial, we'll learn more about Amazon instances: how to configure and launch them, how to connect to them and some basic functions of the command line tools.

# 1. Launch an instance


- Connect to the [Amazon EC2 console](https://console.aws.amazon.com/ec2/)
- Go to the **EC2 dashboard**, click on **Launch instance**.
- Then select the Ubuntu Server AMI.
- Stick to the t2.micro instance (free tier eligible).
- Go to **Configure Security Group** and select the group we configured in [AWS Part 1](../AWS tutorial part 1).
- We are ready to **Launch**
- Select the key pair we created in [AWS Part 1](../AWS tutorial part 1) when prompted. A new key pair can also be created.
- Click **Launch Instances**

**N.B.** Don't select the Proceed without a key pair option. If you launch your instance without a key pair, then you can't connect to it.

**N.B.** It can take some time for the instance to launch. Review its status in **Status Checks** column.


# 2. Connect to your instance with an SSH

- Verify an SSH client is installed on your computer
- Install Amazon CLI tools.

Download the tools from this link
	
	wget http://s3.amazonaws.com/ec2-downloads/ec2-api-tools.zip

And unzip in a suitable directory

	sudo mkdir /usr/local/ec2
	sudo unzip ec2-api-tools.zip -d /usr/local/ec2


## Install and configure JAVA

The Amazon EC2 CLI tools require Java. You can check Java is installed by running 

	which java

which should yield something like :

	/usr/bin/java

If that is not the case, install java as indicated [here](http://askubuntu.com/questions/521145/how-to-install-oracle-java-on-ubuntu-14-04).

We now need to find the Java home directory. The which command we executed earlier returns Java's location in the $PATH environment variable but most of the time, it's a symbolic link.

You can check this by running :

	file $(which java)

which in my case returns :

	/usr/bin/java: symbolic link to `/etc/alternatives/java'

by iterating the file command, you can find the true java home directory :

	file /etc/alternatives/java
	> /etc/alternatives/java: symbolic link to `/usr/lib/jvm/java-8-oracle/jre/bin/java'

the last location is the actual binary, which you can check by running :

	file /usr/lib/jvm/java-8-oracle/jre/bin/java
	> /usr/lib/jvm/java-8-oracle/jre/bin/java: ELF 64-bit LSB  executable

In this example, the java home directory is :

	/usr/lib/jvm/java-8-oracle/jre/

We are now going to set the JAVA_HOME variable to the home directory we identified :

	export JAVA_HOME="/usr/lib/jvm/java-8-oracle/jre/"

To check this has been set correctly, use :

	$JAVA_HOME/bin/java -version

which should get you :

	java version "1.8.0_66"
	Java(TM) SE Runtime Environment (build 1.8.0_66-b17)
	Java HotSpot(TM) 64-Bit Server VM (build 25.66-b17, mixed mode)

Add this variable definition to your .bashrc so that JAVA_HOME is defined whenever you spawn a new shell.

## Set the CLI Tools location

The Amazon EC2 CLI tools read the `EC2_HOME` environment variable to locate supporting libraries. Before using these tools, set EC2_HOME to the directory path where you unzipped them. In your .bashrc, write :

	export EC2_HOME="/usr/local/ec2/ec2-api-tools-1.7.5.1"

where the version number are specific to the version you downloaded. To get the right numbers, use :

	ls /usr/local/ec2

We will also add the bin directory for the CLI tools to our system path. 

	export PATH="$PATH:$EC2_HOME/bin"


## Set your identity for the CLI Tools

Your access keys identify you to the Amazon EC2 CLI tools. There are two types of access keys: access key IDs (for example, AKIAIOSFODNN7EXAMPLE) and secret access keys (for example, wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY). You should have stored your access keys in a safe place when you received them. 

We will set the following environment variable which will serve as default values for the access and secret keys. This will save you from entering your keys for each command.

	export AWS_ACCESS_KEY=your-aws-access-key-id 
	export AWS_SECRET_KEY=your-aws-secret-key

We can check that the keys have been properly set

	ec2-describe-regions

Which should yield something like :

	>REGION	eu-west-1	ec2.eu-west-1.amazonaws.com
	>REGION	ap-southeast-1	ec2.ap-southeast-1.amazonaws.com
	>REGION	ap-southeast-2	ec2.ap-southeast-2.amazonaws.com
	>REGION	eu-central-1	ec2.eu-central-1.amazonaws.com
	>REGION	ap-northeast-1	ec2.ap-northeast-1.amazonaws.com
	>REGION	us-east-1	ec2.us-east-1.amazonaws.com
	>REGION	sa-east-1	ec2.sa-east-1.amazonaws.com
	>REGION	us-west-1	ec2.us-west-1.amazonaws.com
	>REGION	us-west-2	ec2.us-west-2.amazonaws.com


## Change the region (if needed)

The default EC2 CLI region is US East (us-east-1).
To change this region, you need to set the following environment variable

	export EC2_URL=https://<service_endpoint> 

where the service endpoint is something like ec2.region.amazonaws.com (cf `ec2-describe-regions`). 

## Connect via SSH

In a terminal, go to the location of the private key file (.pem) used when launching the instance.
In a command line shell, change directories to the location of the private key file that you created when you launched the instance.

The SSH command should be something like :

	ssh -i /path/my-key-pair.pem user_name@public_dns_name

where use name is `ubuntu` for an ubuntu AMI and the public dns name is specified in the AWS console. Alternatively, the dns name can be found using 

	ec2-describe-instances

For instance :

	ssh -i /path/my-key-pair.pem ubuntu@ec2-52-62-114-212.ap-southeast-2.compute.amazonaws.com

When prompted, enter yes.

You should get something like :

	Welcome to Ubuntu 14.04.2 LTS (GNU/Linux 3.13.0-48-generic x86_64)

	 * Documentation:  https://help.ubuntu.com/

	  System information as of Sun Jan  3 07:11:31 UTC 2016

	  System load: 0.0              Memory usage: 5%   Processes:       82
	  Usage of /:  9.8% of 7.74GB   Swap usage:   0%   Users logged in: 0

	  Graph this data and manage this system at:
	    https://landscape.canonical.com/

	  Get cloud support with Ubuntu Advantage Cloud Guest:
	    http://www.ubuntu.com/business/services/cloud

	0 packages can be updated.
	0 updates are security updates.



	The programs included with the Ubuntu system are free software;
	the exact distribution terms for each program are described in the
	individual files in /usr/share/doc/*/copyright.

	Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
	applicable law.


Congrats, you are now connected !

You can transfer files easily with the scp command :

	scp -i /path/my-key-pair.pem myfile ubuntu@ec2-52-62-114-212.ap-southeast-2.compute.amazonaws.com:~

# 3. Close your an instance

- Select your instance in the AWS console.
- **Actions** , **Instance State**, **Terminate**.
- Choose **Yes, Terminate**.