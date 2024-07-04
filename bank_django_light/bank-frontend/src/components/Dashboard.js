import React, { useEffect, useState } from 'react';
import { Container, Button, Typography, Box, List, ListItem, ListItemText } from '@mui/material';
import { Link } from 'react-router-dom';
import api from '../api';

function Dashboard() {
    const [accounts, setAccounts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchAccounts();
    }, []);

    const fetchAccounts = () => {
        setLoading(true);
        api.get('/accounts/')
            .then(response => {
                setAccounts(response.data);
                setLoading(false);
            })
            .catch(error => {
                setError('Failed to fetch accounts');
                setLoading(false);
            });
    };

    const createAccount = () => {
        const user_id = 1;
        api.post('/accounts/create_account/', { user_id })
            .then(response => {
                fetchAccounts();
            })
            .catch(error => {
                setError('Failed to create account');
            });
    };

    if (loading) {
        return <Typography>Loading...</Typography>;
    }

    if (error) {
        return <Typography>{error}</Typography>;
    }

    return (
        <Container maxWidth="md">
            <Box mt={5}>
                <Typography variant="h4" gutterBottom>Dashboard</Typography>
                <Button onClick={createAccount} variant="contained" color="primary">
                    Create Account
                </Button>
                {accounts.length === 0 ? (
                    <Typography>No accounts available.</Typography>
                ) : (
                    <List>
                        {accounts.map(account => (
                            <ListItem key={account.id} button component={Link} to={`/account/${account.id}`}>
                                <ListItemText primary={`Account: ${account.account_number}, Balance: ${account.balance}`} />
                            </ListItem>
                        ))}
                    </List>
                )}
            </Box>
        </Container>
    );
}

export default Dashboard;
