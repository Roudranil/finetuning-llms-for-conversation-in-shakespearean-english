# Modelling details

- [Modelling details](#modelling-details)
  - [ericzzz/falcon-rw-1b-instruct-openorca](#ericzzzfalcon-rw-1b-instruct-openorca)
    - [Prompt template:](#prompt-template)
  - [togethercomputer/RedPajama-INCITE-Chat-3B-v1](#togethercomputerredpajama-incite-chat-3b-v1)
    - [Prompt template:](#prompt-template-1)
    - [Generated samples](#generated-samples)
  - [mistralai/Mistral-7B-Instruct-v0.2](#mistralaimistral-7b-instruct-v02)
    - [Prompt template](#prompt-template-2)
    - [Generated samples](#generated-samples-1)

As stated in the [README.md](../README.md), I tried finetuning on the following models
| Model name                                                                                                          | Size |
| ------------------------------------------------------------------------------------------------------------------- | ---- |
| [ericzzz/falcon-rw-1b-instruct-openorca](https://huggingface.co/ericzzz/falcon-rw-1b-instruct-openorca)             | $1B$ |
| [togethercomputer/RedPajama-INCITE-Chat-3B-v1](https://huggingface.co/togethercomputer/RedPajama-INCITE-Chat-3B-v1) | $3B$ |
| [mistralai/Mistral-7B-Instruct-v0.2](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2)                     | $7B$ |

## ericzzz/falcon-rw-1b-instruct-openorca 

> [!IMPORTANT]
> Model needs to be trained for longer.

Currently, the model has been trained for a total of 6600 steps, reaching a minimum loss of 1.8. 

### Prompt template:
```python
f"<SYS> {system} <INST> {user} <RESP> {response}"
```

## togethercomputer/RedPajama-INCITE-Chat-3B-v1

> [!IMPORTANT]
> Model needs to be trained for longer.

I trained it for 500 steps, with minimum loss at 2.29. 

### Prompt template:
```python
f"<system>: {system}\n<human>: {user}\n<bot>: {response}"
```

### Generated samples

```
user: How is the weather today?
response:    It is a good day for a storm, a foul day    For a fair weather.  
```

## mistralai/Mistral-7B-Instruct-v0.2

> [!IMPORTANT]
> Model needs to be trained for longer.

I trained it for 2500 steps, as I decided to go longer on a bigger model to see what was really possible. Any longer and the colab runtime disconnects.

### Prompt template
```python
f"<s>[INST] {system}\n\n{user} [/INST] {response} </s>"
```

### Generated samples

I limited the maximum number of new tokens to be generated to be 32 for the first few examples. So some responses get cut-off abruptly.

```
user: Describe the beauty of the mountains
response:  The mountains, like kings, proudly tower over the earth. Their snowy peaks, glistening in the sun, remind us of heaven. The val
```

```
user: Can you tell me about the joys of monsoon?
response: Monsoon, my dear, is a time of heavy rain and strong winds, which bring life back to the land. It's a time of hope

user: But is monsoon better than summer?
response:    Ay, marry, 'tis the best of seasons.   

user: And is monsoon better than winter or spring?
response:     Well, monsoon is the best of all the seasons,    'Tis true: it brings the rain, which is the food    Of our fair land, and makes it fruitful:    The flowers, like ladies, 'gin to look fair;    The orchards and the vineyards begin to flourish;    The cattle and the horses begin to fatten;    And the birds and beasts to be in't:    And 'tis a season of plenty, as you say,    That comes but once a year:   'tis like a jig,    That makes the
```

The last one had a max token limit of 128.