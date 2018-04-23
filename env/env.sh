DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export WORKFLOW_HOME=`echo $DIR | sed 's/\/env//g'`
LIB_CHECK=`ls -alh ${WORKFLOW_HOME}/lib | grep WORKFLOW_CORE | wc -l`

echo ${WORKFLOW_HOME}/lib
echo ${PYTHONPATH}
if [ "${LIB_CHECK}" -eq "0" ]
then
    export PYTHONPATH=${WORKFLOW_HOME}/lib:${PYTHONPATH}
else
    export PYTHONPATH=${WORKFLOW_HOME}/lib/EVENTFLOW_CORE.zip:${PYTHONPATH}
fi
   
