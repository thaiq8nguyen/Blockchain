import React, { useEffect, useState } from "react";
import { Button, Card, Container, Form, Grid, Header } from "semantic-ui-react";
import axios from "axios";

const User = () => {
  const [sender, setSender] = useState("Thai");
  const [recipient, setRecipient] = useState("");
  const [amount, setAmount] = useState(0);
  const [newTransaction, setNewTransaction] = useState(false);
  const [balance, setBalance] = useState(0);

  useEffect(() => {
    axios.get("http://localhost:5000/chain").then(response => {
      let transactionArray = response.data.chain.map(el => el.transactions);
      let transactions = [];
      for (let i = 0; i < response.data.chain.length; i++) {
        transactions = transactions.concat(transactionArray[i]);
      }
      let tempBalance = balance;
      transactions.forEach(transaction => {
        if (transaction.sender === sender) {
          tempBalance -= transaction.amount;
        }
      });

      setBalance(tempBalance);
    });
  }, []);

  useEffect(() => {
    if (newTransaction) {
      axios.get("http://localhost:5000/chain").then(response => {
        setNewTransaction(false);
      });
    }
  }, [newTransaction]);

  const handleFormSubmit = () => {
    //console.log(sender);
    axios
      .post("http://localhost:5000/transactions/new", {
        sender,
        recipient,
        amount
      })
      .then(response => {
        setNewTransaction(true);
        clearTransactionForm();
      });
  };
  const clearTransactionForm = () => {
    setSender("");
    setRecipient("");
    setAmount(0);
  };

  const handleInputChange = e => {
    if (e.target.name === "sender") {
      setSender(e.target.value);
    } else if (e.target.name === "recipient") {
      setRecipient(e.target.value);
    } else {
      setAmount(e.target.value);
    }
  };
  return (
    <div>
      <Grid>
        <Grid.Row columns={3}>
          <Grid.Column>
            <Card>
              <Card.Content>
                <Card.Header>Current Balance</Card.Header>
              </Card.Content>
              <Card.Description>Balance: {balance}</Card.Description>
            </Card>
          </Grid.Column>
          <Grid.Column>
            <Card>
              <Card.Content>
                <Card.Header>Transactions</Card.Header>
              </Card.Content>
              <Card.Content>
                <Header>Create Transaction</Header>
                <Form onSubmit={handleFormSubmit}>
                  <Form.Input
                    label="Sender"
                    placeholder="Sender's Name"
                    value={sender}
                    onChange={handleInputChange}
                    name="sender"
                  />
                  <Form.Input
                    label="Recipient"
                    placeholder="Recipient's Name"
                    value={recipient}
                    onChange={handleInputChange}
                    name="recipient"
                  />

                  <Form.Input
                    label="Amount"
                    placeholder="Amount"
                    value={amount}
                    onChange={handleInputChange}
                    name="amount"
                  />
                  <Button type="submit">Submit</Button>
                </Form>
              </Card.Content>
            </Card>
          </Grid.Column>
          <Grid.Column>User Profile</Grid.Column>
        </Grid.Row>
      </Grid>
    </div>
  );
};

export default User;
