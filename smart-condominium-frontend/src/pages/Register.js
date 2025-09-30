// Smart Condominium - Página de Registro
import React, { useState } from 'react';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import {
  Container,
  Paper,
  Box,
  Typography,
  TextField,
  Button,
  Link,
  Grid,
  Alert,
} from '@mui/material';
import { Business } from '@mui/icons-material';
import { motion } from 'framer-motion';

import { useAuth } from '../contexts/AuthContext';
import LoadingSpinner from '../components/common/LoadingSpinner/LoadingSpinner';

const Register = () => {
  const navigate = useNavigate();
  const { register, loading, error } = useAuth();

  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    first_name: '',
    last_name: '',
  });
  const [formErrors, setFormErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
    
    if (formErrors[name]) {
      setFormErrors(prev => ({
        ...prev,
        [name]: '',
      }));
    }
  };

  const validateForm = () => {
    const errors = {};
    
    if (!formData.username.trim()) {
      errors.username = 'El usuario es requerido';
    }
    
    if (!formData.email.trim()) {
      errors.email = 'El email es requerido';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'Email inválido';
    }
    
    if (!formData.password.trim()) {
      errors.password = 'La contraseña es requerida';
    } else if (formData.password.length < 6) {
      errors.password = 'La contraseña debe tener al menos 6 caracteres';
    }
    
    if (formData.password !== formData.confirmPassword) {
      errors.confirmPassword = 'Las contraseñas no coinciden';
    }
    
    if (!formData.first_name.trim()) {
      errors.first_name = 'El nombre es requerido';
    }
    
    if (!formData.last_name.trim()) {
      errors.last_name = 'El apellido es requerido';
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    const { confirmPassword, ...registerData } = formData;
    const result = await register(registerData);
    
    if (result.success) {
      navigate('/dashboard');
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #1565C0 0%, #0D47A1 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        p: 2,
      }}
    >
      <Container maxWidth="md">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <Paper
            elevation={10}
            sx={{
              p: 4,
              borderRadius: 3,
              background: 'rgba(255, 255, 255, 0.95)',
              backdropFilter: 'blur(10px)',
            }}
          >
            {/* Logo y título */}
            <Box sx={{ textAlign: 'center', mb: 4 }}>
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ duration: 0.5, delay: 0.2 }}
              >
                <Business 
                  sx={{ 
                    fontSize: 60, 
                    color: 'primary.main',
                    mb: 2,
                  }} 
                />
              </motion.div>
              
              <Typography 
                variant="h4" 
                component="h1" 
                gutterBottom
                sx={{ 
                  fontWeight: 700,
                  background: 'linear-gradient(45deg, #1565C0, #0D47A1)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
              >
                Crear Cuenta
              </Typography>
              
              <Typography variant="subtitle1" color="text.secondary">
                Únete a Smart Condominium
              </Typography>
            </Box>

            {/* Formulario de registro */}
            <Box component="form" onSubmit={handleSubmit} noValidate>
              {error && (
                <Alert severity="error" sx={{ mb: 3 }}>
                  {error}
                </Alert>
              )}

              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    name="first_name"
                    label="Nombre"
                    value={formData.first_name}
                    onChange={handleChange}
                    error={!!formErrors.first_name}
                    helperText={formErrors.first_name}
                    disabled={loading}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    name="last_name"
                    label="Apellido"
                    value={formData.last_name}
                    onChange={handleChange}
                    error={!!formErrors.last_name}
                    helperText={formErrors.last_name}
                    disabled={loading}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    name="username"
                    label="Nombre de Usuario"
                    value={formData.username}
                    onChange={handleChange}
                    error={!!formErrors.username}
                    helperText={formErrors.username}
                    disabled={loading}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    name="email"
                    label="Email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    error={!!formErrors.email}
                    helperText={formErrors.email}
                    disabled={loading}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    name="password"
                    label="Contraseña"
                    type="password"
                    value={formData.password}
                    onChange={handleChange}
                    error={!!formErrors.password}
                    helperText={formErrors.password}
                    disabled={loading}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    name="confirmPassword"
                    label="Confirmar Contraseña"
                    type="password"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    error={!!formErrors.confirmPassword}
                    helperText={formErrors.confirmPassword}
                    disabled={loading}
                  />
                </Grid>
              </Grid>

              <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                disabled={loading}
                sx={{ 
                  mt: 3, 
                  mb: 2, 
                  height: 48,
                  fontSize: '1.1rem',
                  fontWeight: 600,
                }}
              >
                {loading ? <LoadingSpinner size={24} /> : 'Crear Cuenta'}
              </Button>

              <Box sx={{ textAlign: 'center' }}>
                <Link
                  component={RouterLink}
                  to="/login"
                  variant="body2"
                  sx={{ textDecoration: 'none' }}
                >
                  ¿Ya tienes cuenta? Inicia sesión aquí
                </Link>
              </Box>
            </Box>
          </Paper>
        </motion.div>
      </Container>
    </Box>
  );
};

export default Register;