#!/bin/bash

python_cmd=`which python`
find_cmd=`which find`



if [ -z "${EVENTFLOW_HOME}" ]
then
    TEMP_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    EVENTFLOW_HOME=`echo ${TEMP_PATH} | sed 's/setup//g'`
fi

SETUP_PATH=${EVENTFLOW_HOME}/setup
LIB_PATH=${EVENTFLOW_HOME}/lib

empty_space(){
    echo ""
    echo ""
}

setup_env()
{
    empty_space
    echo "## env setting start"
    BASH_CHECK=`cat ~/.bashrc | grep ${WORKFLOW_HOME} | wc -l`
    if [ "${BASH_CHECK}" -eq "0" ]
    then
        echo "source ${WORKFLOW_HOME}/env/env.sh" >> ~/.bashrc
        echo "env set complete"
    else
        echo "env is already setted"
    fi
    echo "## env setting end"
    empty_space
}

compile()
{
    empty_space
    echo "## compile lib directory start"
    ${python_cmd} -c "import compileall;compileall.compile_dir('${LIB_PATH}',maxlevels=10)"
    echo "## compile lib directory end"
    empty_space
}

removePY(){
    empty_space
    echo "## py clean process start"
    ${find_cmd} ${LIB_PATH} -name *.py | xargs rm
    echo "## clean process end"
    empty_space
}

removePYC(){
    empty_space
    echo "## pyc clean process start"
    ${find_cmd} ${LIB_PATH} -name *.pyc | xargs rm
    echo "## clean process end"
    empty_space
}

archive(){
    empty_space
    echo "## archive start"
    ZIP_CHECK=`ls -alh ${LIB_PATH}/*.zip 2> /dev/null | wc -l`
    if [ "${ZIP_CHECK}" != "0" ]
    then
        echo "zip file is already exist"
    else
        GIT_REVISION=`git rev-parse HEAD`
        GIT_TAG=`git describe --tags 2> /dev/null`
        if [ -z "${GIT_REVISION}" ]
        then
            GIT_REVISION="00000"
        fi
        if [ -z "${GIT_TAG}" ]
        then
            GIT_TAG="DEFAULT"
        fi
        FILE_NAME="EVENTFLOW_CORE_${GIT_TAG}_${GIT_REVISION:0:5}.zip"
        cd ${LIB_PATH} && zip -r0 ${FILE_NAME} EventFlow -i *.pyc
        cd ${LIB_PATH} && ln -s ${FILE_NAME} EVENTFLOW_CORE.zip
    fi
    echo "## archive end"
    empty_space
}

removeZIP(){
    empty_space
    echo "## remove old zip start"
    rm ${LIB_PATH}/*.zip
    echo "## remove old zip end"
    empty_space
}

removeSRC(){
    empty_space
    echo "## remove src start"
    rm -r ${LIB_PATH}/EventFlow
    echo "## remove src end"
    empty_space
}




case $1 in
    'env')
        empty_space
        echo "# setup program start with option $1"
        echo "# wait 5 sec for cancel. if you want cancel 'Ctrl + c'"
        empty_space
        sleep 5
        setup_env
        echo "# all process ${1} end";;
    'compile')
        empty_space
        echo "# setup program start with option $1"
        echo "# wait 5 sec for cancel. if you want cancel 'Ctrl + c'"
        empty_space
        sleep 5
        removePYC
        compile
        echo "# all process ${1} end";;
    'clean')
        empty_space
        echo "# setup program start with option $1"
        echo "# wait 5 sec for cancel. if you want cancel 'Ctrl + c'"
        empty_space
        sleep 5
        removePYC
        echo "# all process ${1} end";;
    'archive')
        empty_space
        echo "# setup program start with option $1"
        echo "# wait 5 sec for cancel. if you want cancel 'Ctrl + c'"
        empty_space
        sleep 5
        archive
        echo "# all process ${1} end";;
    'for_sale')
        empty_space
        echo "# setup program start with option $1"
        echo "# wait 5 sec for cancel. if you want cancel 'Ctrl + c'"
        empty_space
        sleep 5
        removePYC
        removeZIP
        compile
        removePY
        archive
        removeSRC
        echo "# all process ${1} end";;
    'install')
        empty_space
        echo "# setup program start with option $1"
        echo "# wait 5 sec for cancel. if you want cancel 'Ctrl + c'"
        empty_space
        sleep 5
        setup_env
        echo "# all process ${1} end";;
    *)
        echo "Usage : ${0} [install | for_sale | archive | clean | compile | env]"
esac
