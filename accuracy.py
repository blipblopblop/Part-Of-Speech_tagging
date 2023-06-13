import argparse

def create_trainingList(training_list):
    list_train = training_list.split('\n')
    trainingList = []
    for currLine in list_train:
        line = currLine.split(' : ') 
        if len(line) == 2:
            # passing into the global trainingList variable
            trainingList.append(line)
    
    return trainingList

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--acc",
        action="append",
        nargs="+",
        required=True,
        help="The training files."
    )
    parser.add_argument(
        "--test",
        type=str,
        required=True,
        help="One test file."
    )
    args = parser.parse_args()

    accs = args.acc[0]
    print("acc file is {}".format(accs))
    print("test file is {}".format(args.test))

    
    s=''
    for filename in accs:
        f=open(filename)
        s=s+f.read().replace('\r\n','\n')+'\n'      # if made in windows its '\r\n' with '\n'
        f.close()
    trainingList = create_trainingList(s)

    test_file = open(args.test)
    test = test_file.read().replace('\r\n','\n')+'\n'      # if made in windows its '\r\n' with '\n'
    test_file.close()

    testList = create_trainingList(test)
    #print(trainingList, testList)

    accs = 0
    for i in range(len(testList)):
        if testList[i] == trainingList[i]:
            accs += 1

    print(accs/(len(testList)))


    


