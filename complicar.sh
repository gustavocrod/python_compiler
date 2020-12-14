PYTHON="python3"
COMPILER="complicador.py"
CC="gcc"

BN=$(basename -s .cmp $1)

COMPLICADOROUTPUT=$(${PYTHON} ${COMPILER} -i $1 -o $BN.c)
CCOUTPUT=$(${CC} -o ${BN} ${BN}.c)
if [ $? -ne 0 ]; then
    echo "${CCOUTPUT}"
else
    echo "${COMPLICADOROUTPUT}"
fi

echo "Agora é só rodar ./${BN}"