from paramiko import SSHClient
from scp import SCPClient
import sys
from string import ascii_lowercase

# Define progress callback that prints the current percentage completed for the file
def progress(filename, size, sent):
    sys.stdout.write("%s\'s progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )

for i in ['a', 'b', 'c']:
	for j in ascii_lowercase:
		print(i, j)
		if not (i=='a'): #and (j in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])):
			ssh = SSHClient()
			ssh.load_system_host_keys()
			ssh.connect(hostname='datascience5.cs.man.ac.uk', username='n82471zk', password='Muramura10!')
			scp = SCPClient(ssh.get_transport(), progress=progress)
			
			print('project_dataset.zip.part'+i+j)
			
			try:
				scp.put('/home/deadman/Uni/project/dataset/project_dataset.zip.part'+i+j, '/local/home/n82471zk/project_dataset/project_dataset.zip.part'+i+j)
			except:
				print('fail')
				scp.close()
				ssh.close()
				continue
				
				
			
			scp.close()
			ssh.close()
			
