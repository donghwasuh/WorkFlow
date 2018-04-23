DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export EVENTFLOW_HOME=`echo $DIR | sed 's/\/env//g'`
LIB_CHECK=`ls -alh ${EVENTFLOW_HOME}/lib | grep EVENTFLOW_CORE | wc -l`

if [ "${LIB_CHECK}" -eq "0" ]
then
    export PYTHONPATH=${EVENTFLOW_HOME}/lib:${PYTHONPATH}
else
    export PYTHONPATH=${EVENTFLOW_HOME}/lib/EVENTFLOW_CORE.zip:${PYTHONPATH}
fi
    
