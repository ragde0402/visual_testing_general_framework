import java.text.SimpleDateFormat;
import java.util.Date;

microservices = ["EXAMPLE"] // add all your microservices names
environments = ["ENV", "ENV1"]
sources = ["svn", "ftp", "zip"]
pickedMicroservices = []
choices = ["Take screenshots and save in SVN", "Compare screenshots"]
projectName = "Your project name"
svnRoot = "add your svn url"
fileNameDate= new SimpleDateFormat("yyyy-MMM-dd_HH_mm").format(new Date())
folderNameYear= new SimpleDateFormat("yyyy").format(new Date())
folderNameMonth= new SimpleDateFormat("MMM").format(new Date())
filenamecsv= "${fileNameDate}_results.csv"
filenamehtml= "${fileNameDate}_results.html"
archive="${folderNameYear}_${currentBuild.number}"

pipeline{
    parameters{
        choice(name:'choice', choices: choices, description: 'Choose what to do.')
        choice(name:'environment', choices: environments, description: 'Choose environment')
        choice(name:'source', choices: sources, description: 'Choose source')
        booleanParam(defaultValue: true, name: "Publish", description: "Publish report")
        booleanParam(defaultValue: true, name: 'EXAMPLE', description: 'Example') // add booleanParam for all that in microservices list
    }

    agent {
        node { label "label" } // use label that exists in your project for agent that you want to use
    }
    stages {
        stage('Preparation'){
            steps{
                script{
                    params.each {
                        param -> if (param.value == true && microservices.contains(param.key)){
                        pickedMicroservices.add(param.key)
                        }
                    println(pickedMicroservices)
                    }
//                  It is highly possible that first two install will not be required in your jenkins,
//                  but sometimes there is some error. If you want to test everything local remember to also install
//                  subversion like in last line of sh command
                    sh """
                    sudo apt install libgl1-mesa-glx -y
                    sudo apt-get install libglib2.0-0 -y
                    python3 -m pip install --upgrade pip
                    python3 -m pip install -r requirements.txt
                    sudo apt-get install subversion -y
                    """
					
					createFolder(archive)
                }
            }
        }
		stage('svn preparation'){
            when {
                expression { return params.source == "svn" }
            }
            steps{
                withCredentials([usernamePassword(credentialsId: 'CREDS_ID', passwordVariable: 'PWS', usernameVariable: 'USER')]) {
					    script {
					        def svn_path = tool name: 'subversion', type: 'com.cloudbees.jenkins.plugins.customtools.CustomTool'
						    sh("svn --username ${USER} --password ${PWS} import -m \'Auto folder generation\' ./${archive}/ ${svnRoot}/archive/${archive}")
                    }
                }
            }
		}
        stage('Screenshots creation'){
            when {
                expression { return params.choice == "Take screenshots and save in SVN"}
            }
            steps{
                withCredentials([usernamePassword(credentialsId: 'CREDS_ID', passwordVariable: 'PWS', usernameVariable: 'USER')])  {
                    script{
                        for (service in pickedMicroservices){
                                sh("python3 main.py -s ${svnRoot} -u ${USER} -p ${PWS} -n ${service} -m 'new_screenshots' -e ${params.environment} -d ${params.source}")
                            }
                        }
                    }
                }
            }
        stage('Compare screenshots'){
            when {
                expression {return params.choice == "Compare screenshots"}
            }
            steps{
                withCredentials([usernamePassword(credentialsId: 'CREDS_ID', passwordVariable: 'PWS', usernameVariable: 'USER')])  {
                    script{
                        def documentcsv = "SERVICE;PAGE;RESULT \n"
                        writeFile file: filenamecsv, text: documentcsv
                        stash includes: filenamecsv, name: 'results2'
                        for (service in pickedMicroservices){
                                sh("python3 main.py -s ${svnRoot} -u ${USER} -p ${PWS} -n ${service} -m 'check_screenshots' -c ${filenamecsv} -a \"${archive}\" -e ${params.environment}")
                            }
//                             Depending on permissions: you can use simply csv readFile or you need to workaround like it is shown
                        sh"""
                            cat ${filenamecsv}
                            """
                        resultString = sh(returnStdout:true,script:"cat ${filenamecsv}").trim()
                        println(resultString)
                        }
                    }
                }
            }
        stage('Create HTML report') {
		    when {
                expression {return params.choice == "Compare screenshots"}
            }
			steps {
				script{
                    def resultMap = [:]
                    def lines = resultString.split('\n')
                    for (line in lines){
                        def values = line.split(',')
                        if(values.size() == 3) { 
                            if (resultMap[values[0]] == null) {
                                resultMap[values[0]] = []
                            }
                            resultMap[values[0]].push([values[1], values[2]])
                        }
                    }
					generateHTML(resultMap)

                }
            }
        }
        
        stage('Publish to Confluence') {
		    when {
                expression {return params.choice == "Compare screenshots" && params.Publish}
            }
            steps{
                publishConfluence attachArchivedArtifacts: false, buildIfUnstable: true, editorList: [confluenceWritePage(confluenceText(readFile(filenamehtml)))], pageName: 'Visual Testing', parentId: YourParentID, replaceAttachments: false, siteName: 'yourSiteName', spaceName: 'YourSpaceName'
            }
        }

		stage('Archive results'){
            when {
                expression {return params.choice == "Compare screenshots"}
            }
			steps{
				script{

                sh "mv ${filenamecsv} ./${archive}/"
				sh "mv ${filenamehtml} ./${archive}/"

				withCredentials([usernamePassword(credentialsId: 'CREDS_ID', passwordVariable: 'PWS', usernameVariable: 'USER')]) {
    			sh("svn --username ${USER} --password ${PWS} import -m 'Archive files' ./${archive}/ ${svnRoot}/archive/${archive}")
                }
			
				archiveArtifacts "${archive}/${filenamehtml}"
				archiveArtifacts "${archive}/${filenamecsv}"
			 	}	
			}
		}		
        
        stage('cleanup'){
			steps{
                cleanWs notFailBuild: true
			    }
		    }
        }
    }

def listFolder(){
  if(isUnix()){
    sh 'ls -l'
  }else{
    bat 'dir'
  }
}

def createFolder(String __folder_name){
  if(!fileExists(__folder_name)){
    if(isUnix()){
      sh "mkdir -p ${__folder_name}"
    }
    else {
      bat "mkdir ${__folder_name}"
    }
  }
}

def generateHTML(resultsMap){
    def document = "<html>"
	document+="<head><title>Report</title></head><body>"
    resultsMap.each{
        k,v ->
        document+="<table>"
        document+="<h3>${k}</h3>"
        document+="<tr><th>Page</th><th>Result</th></tr>"
        v.each{
            item -> 
			Float valParsedToFloat = item[1]
				if(valParsedToFloat < 0.99) 
					{document+="<tr style=\"background-color:#FF0000\"><td>${item[0]}</td><td>${item[1]}</td></tr>"}
				else 
					{document+="<tr><td>${item[0]}</td><td>${item[1]}</td></tr>"}
            
			
        }
        document+="</table>"
    }
    document += "</body><br/><a href=\"${svnRoot}/archive/${archive}\">SVN: ${svnRoot}/archive/${archive}</a></html>"
    writeFile file: filenamehtml, text: document
    stash includes: filenamehtml, name: 'results'

}
