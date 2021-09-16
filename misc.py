import jsonlines

#%%
def test1():
    # create some test data for doccano
    data = []
    data.append(
        {
            'text': 'this is a test file',
            'label': ['relevant', 'irrelevant']
        }
    )
    data.append(
        {
            'text': 'new test file',
            'label': ['relevant', 'irrelevant']
        }
    )
    with jsonlines.open('doccano_test.jsonl', 'w') as writer:
        for obj in data:
            writer.write(obj)

    print('saved')


if __name__ == '__main__':
    test1()


