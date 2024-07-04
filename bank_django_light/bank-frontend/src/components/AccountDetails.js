import React, { useEffect, useState } from 'react';
import { Container, Typography, Box, Button, TextField } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';

function AccountDetails() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [account, setAccount] = useState(null);
    const [amount, setAmount] = useState('');
    const [error, setError] = useState(null);

    useEffect(() => {
        api.get(`/accounts/${id}/`)
            .then(response => {
                setAccount(response.data);
            })
            .catch(error => {
                setError('Failed to fetch account details');
            });
    }, [id]);

    const handleDeposit = () => {
        api.post(`/accounts/${id}/deposit/`, { amount })
            .then(response => {
                setAccount(response.data);
                setAmount('');
                setError(null);
            })
            .catch(error => {
                setError('Failed to deposit');
            });
    };

    const handleWithdraw = () => {
        api.post(`/accounts/${id}/withdraw/`, { amount })
            .then(response => {
                setAccount(response.data);
                setAmount('');
                setError('Transaction Successful');
            })
            .catch(error => {
                setError(`Failed to withdraw: ${error.response.data.error}`);
            });
    };

    const handleTransfer = () => {
        navigate("/transfer");
    };

    const handleDelete = () => {
        api.delete(`/accounts/${id}/`)
            .then(() => {
                navigate('/dashboard');
            })
            .catch(error => {
                setError('Failed to delete account');
            });
    };

    return (
        <Container maxWidth="sm">
            <Box mt={5}>
                {error && <Typography color="error">{error}</Typography>}
                {account ? (
                    <>
                        <Typography variant="h4" gutterBottom>Account Details</Typography>
                        <Typography variant="h6">Account Number: {account.account_number}</Typography>
                        <Typography variant="h6">Balance: {account.balance}</Typography>
                        <Box mt={3}>
                            <TextField
                                label="Amount"
                                value={amount}
                                onChange={(e) => setAmount(e.target.value)}
                                fullWidth
                                margin="normal"
                            />
                            <Button variant="contained" color="primary" onClick={handleDeposit} fullWidth>
                                Deposit
                            </Button>
                            <Button variant="contained" color="secondary" onClick={handleWithdraw} fullWidth>
                                Withdraw
                            </Button>
                            <Button variant="contained" color="warning" onClick={handleTransfer} fullWidth>
                                Transfer Money
                            </Button>
                            <Button variant="contained" color="error" onClick={handleDelete} fullWidth>
                                Delete Account
                            </Button>
                        </Box>
                    </>
                ) : (
                    <Typography>Loading...</Typography>
                )}
            </Box>
        </Container>
    );
}

export default AccountDetails;
