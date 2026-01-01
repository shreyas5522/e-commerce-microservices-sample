
import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Chip from '@mui/material/Chip';
import Paper from '@mui/material/Paper';
import Link from '@mui/material/Link';
import StarIcon from '@mui/icons-material/Star';
import axiosClient, { productsUrl } from '../../api/config';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

type Deal = {
  dealId: string | number;
  variantSku: string;
  thumbnail: string;
  name: string;
  shortDescription: string;
  price: number;
  rating: number;
};

const Deals = () => {
  const navigate = useNavigate();

  const [deals, setDeals] = useState<Deal[]>([]);
  const [error, setError] = useState<unknown>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const toArray = <T,>(x: unknown): T[] => (Array.isArray(x) ? (x as T[]) : []);

  const loadDeals = async () => {
    try {
      setLoading(true);
      const response = await axiosClient.get(productsUrl + 'deals');

      // Normalize common payload shapes
      const payload = response?.data;
      const normalized: Deal[] =
        Array.isArray(payload)
          ? payload
          : Array.isArray(payload?.items)
          ? payload.items
          : Array.isArray(payload?.data)
          ? payload.data
          : toArray<Deal>(payload);

      setDeals(normalized);
      setError(null);
    } catch (err) {
      setError(err);
      setDeals([]); // ensure render-safe
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDeals();
  }, []);

  return (
    <Paper elevation={3} sx={{ pl: 2, pb: 2 }}>
      <Typography variant="h6" sx={{ p: 1, color: 'text.primary' }}>
        Deals of the Day
      </Typography>

      {loading && (
        <Typography sx={{ px: 2, pb: 2 }} color="text.secondary">
          Loading deals…
        </Typography>
      )}

      {error && !loading && (
        <Typography sx={{ px: 2, pb: 2 }} color="error">
          Failed to load deals.
        </Typography>
      )}

      <Grid container spacing={2}>
        {deals.slice(0, 5).map((deal) => (
          <Grid item key={deal.dealId ?? deal.variantSku}>
            <Link
              component="button"
              onClick={() => {
                navigate('product/' + deal.variantSku);
              }}
              underline="none"
            >
              <Card sx={{ width: 250, height: 290 }}>
                <Box>
                  <img src={deal.thumbnail} height={150} alt={deal.name} />
                </Box>
                <CardContent sx={{ height: 50 }}>
                  <Grid container>
                    <Grid item xs={12}>
                      <Typography color="text.secondary">
                        {deal.shortDescription}
                      </Typography>
                    </Grid>
                  </Grid>
                </CardContent>
                <CardActions>
                  <Grid container>
                    <Grid item xs={6} sx={{ p: 1, display: 'flex', justifyContent: 'flex-start' }}>
                      <Typography variant="h6">$ {deal.price}</Typography>
                    </Grid>
                    <Grid item xs={6} sx={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center' }}>
                      <Chip icon={<StarIcon />} label={deal.rating} />
                    </Grid>
                  </Grid>
                </CardActions>
              </Card>
            </Link>
          </Grid>
        ))}
      </Grid>
    </Paper>
  );
};

export default Deals;
