// Smart Condominium - Página 404
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography, Button, Paper } from '@mui/material';
import { Home, ArrowBack } from '@mui/icons-material';
import { motion } from 'framer-motion';

const NotFound = () => {
  const navigate = useNavigate();

  const handleGoHome = () => {
    navigate('/dashboard');
  };

  const handleGoBack = () => {
    navigate(-1);
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
        p: 2,
      }}
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.6 }}
      >
        <Paper
          sx={{
            p: 6,
            textAlign: 'center',
            maxWidth: 500,
            borderRadius: 3,
            boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
          }}
        >
          <motion.div
            initial={{ y: -20 }}
            animate={{ y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <Typography
              variant="h1"
              sx={{
                fontSize: { xs: '8rem', md: '12rem' },
                fontWeight: 'bold',
                color: 'primary.main',
                lineHeight: 1,
                mb: 2,
              }}
            >
              404
            </Typography>
          </motion.div>

          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 600 }}>
              Página no encontrada
            </Typography>

            <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
              Lo sentimos, la página que está buscando no existe o ha sido movida.
            </Typography>

            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
              <Button
                variant="contained"
                startIcon={<Home />}
                onClick={handleGoHome}
                size="large"
              >
                Ir al Dashboard
              </Button>

              <Button
                variant="outlined"
                startIcon={<ArrowBack />}
                onClick={handleGoBack}
                size="large"
              >
                Volver Atrás
              </Button>
            </Box>
          </motion.div>
        </Paper>
      </motion.div>
    </Box>
  );
};

export default NotFound;