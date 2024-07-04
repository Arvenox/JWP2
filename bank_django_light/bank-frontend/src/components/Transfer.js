import React, { useState } from 'react';
import { Container, TextField, Button, Typography, Box } from '@mui/material';
import api from '../api';

function Transfer() {
    const [sourceAccount, setSourceAccount] = useState('');
    const [targetAccount, setTargetAccount] = useState('');
    const [amount, setAmount] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        api.post(`/accounts/${sourceAccount}/transfer/`, {
            target_account_number: targetAccount,
            amount,
        }).then(response => {
            setMessage('Transfer successful');
            setSourceAccount('');
            setTargetAccount('');
            setAmount('');
        }).catch(error => {
            setMessage('Failed to transfer');
        });
    };

    return (
        <Container maxWidth="sm">
            <Box mt={5}>
                <Typography variant="h4" gutterBottom>Transfer</Typography>
                <form onSubmit={handleSubmit}>
                    <TextField
                        label="Source Account Number"
                        value={sourceAccount}
                        onChange={(e) => setSourceAccount(e.target.value)}
                        fullWidth
                        margin="normal"
                    />
                    <TextField
                        label="Target Account Number"
                        value={targetAccount}
                        onChange={(e) => setTargetAccount(e.target.value)}
                        fullWidth
                        margin="normal"
                    />
                    <TextField
                        label="Amount"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        fullWidth
                        margin="normal"
                    />
                    <Button variant="contained" color="primary" type="submit" fullWidth>
                        Transfer
                    </Button>
                </form>
                {message && <Typography color="error">{message}</Typography>}
            </Box>
        </Container>
    );
}

export default Transfer;
