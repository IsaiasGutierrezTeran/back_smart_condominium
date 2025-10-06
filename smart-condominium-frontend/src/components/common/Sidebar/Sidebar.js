// Smart Condominium - Sidebar de navegación
import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  Box,
  Typography,
  Collapse,
} from '@mui/material';
import {
  Dashboard,
  AccountBalanceWallet,
  Campaign,
  EventAvailable,
  Security,
  Build,
  ExpandLess,
  ExpandMore,
  Person,
  AdminPanelSettings,
  Groups,
  Assignment,
  Notifications,
  CalendarToday,
  Shield,
  Engineering,
} from '@mui/icons-material';

import { useAuth } from '../../../contexts/AuthContext';
import { DRAWER_WIDTH } from '../../../utils/constants';

const Sidebar = ({ open, onClose, variant = 'persistent' }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, isAdmin, getUserRole } = useAuth();

  const [expandedMenus, setExpandedMenus] = React.useState({});

  const handleMenuClick = (path) => {
    navigate(path);
    if (variant === 'temporary') {
      onClose();
    }
  };

  const handleExpandClick = (menuKey) => {
    setExpandedMenus(prev => ({
      ...prev,
      [menuKey]: !prev[menuKey],
    }));
  };

  const isActive = (path) => {
    return location.pathname.startsWith(path);
  };

  // Elementos del menú principal
  const mainMenuItems = [
    {
      path: '/dashboard',
      label: 'Dashboard',
      icon: <Dashboard />,
      roles: ['administrador', 'residente', 'seguridad', 'mantenimiento'],
    },
  ];

  // Elementos del menú por módulos
  const moduleMenuItems = [
    {
      key: 'finance',
      path: '/finance',
      label: 'Finanzas',
      icon: <AccountBalanceWallet />,
      roles: ['administrador', 'residente'],
      subItems: [
        { path: '/finance/payments', label: 'Mis Pagos', icon: <Assignment /> },
        { path: '/finance/history', label: 'Historial', icon: <Assignment /> },
        ...(isAdmin() ? [
          { path: '/finance/admin', label: 'Administrar', icon: <AdminPanelSettings /> },
          { path: '/finance/reports', label: 'Reportes', icon: <Assignment /> },
        ] : []),
      ],
    },
    {
      key: 'communication',
      path: '/communication',
      label: 'Comunicación',
      icon: <Campaign />,
      roles: ['administrador', 'residente'],
      subItems: [
        { path: '/communication/news', label: 'Noticias', icon: <Notifications /> },
        { path: '/communication/announcements', label: 'Avisos', icon: <Campaign /> },
        ...(isAdmin() ? [
          { path: '/communication/manage', label: 'Gestionar', icon: <AdminPanelSettings /> },
        ] : []),
      ],
    },
    {
      key: 'reservations',
      path: '/reservations',
      label: 'Reservas',
      icon: <EventAvailable />,
      roles: ['administrador', 'residente'],
      subItems: [
        { path: '/reservations/book', label: 'Hacer Reserva', icon: <CalendarToday /> },
        { path: '/reservations/my-reservations', label: 'Mis Reservas', icon: <Assignment /> },
        { path: '/reservations/spaces', label: 'Espacios', icon: <EventAvailable /> },
        ...(isAdmin() ? [
          { path: '/reservations/manage', label: 'Administrar', icon: <AdminPanelSettings /> },
        ] : []),
      ],
    },
    {
      key: 'security',
      path: '/security',
      label: 'Seguridad',
      icon: <Security />,
      roles: ['administrador', 'seguridad'],
      subItems: [
        { path: '/security/visitors', label: 'Visitantes', icon: <Groups /> },
        { path: '/security/vehicles', label: 'Vehículos', icon: <Security /> },
        { path: '/security/incidents', label: 'Incidentes', icon: <Shield /> },
        { path: '/security/access', label: 'Control de Acceso', icon: <Security /> },
        ...(isAdmin() ? [
          { path: '/security/reports', label: 'Reportes', icon: <Assignment /> },
        ] : []),
      ],
    },
    {
      key: 'maintenance',
      path: '/maintenance',
      label: 'Mantenimiento',
      icon: <Build />,
      roles: ['administrador', 'residente', 'mantenimiento'],
      subItems: [
        { path: '/maintenance/requests', label: 'Solicitudes', icon: <Engineering /> },
        { path: '/maintenance/my-requests', label: 'Mis Solicitudes', icon: <Assignment /> },
        ...(isAdmin() || getUserRole() === 'mantenimiento' ? [
          { path: '/maintenance/manage', label: 'Gestionar', icon: <AdminPanelSettings /> },
          { path: '/maintenance/reports', label: 'Reportes', icon: <Assignment /> },
        ] : []),
      ],
    },
  ];

  // Filtrar elementos según el rol del usuario
  const filteredMainItems = mainMenuItems.filter(item => 
    item.roles.includes(getUserRole())
  );

  const filteredModuleItems = moduleMenuItems.filter(item => 
    item.roles.includes(getUserRole())
  );

  const drawerContent = (
    <Box sx={{ overflow: 'auto', height: '100%' }}>
      {/* Información del usuario */}
      <Box sx={{ p: 2, mt: 8 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Person sx={{ mr: 1, color: 'primary.main' }} />
          <Box>
            <Typography variant="subtitle2" noWrap>
              {user ? `${user.first_name} ${user.last_name}` : 'Usuario'}
            </Typography>
            <Typography variant="caption" color="text.secondary" noWrap>
              {user?.rol ? user.rol.charAt(0).toUpperCase() + user.rol.slice(1) : 'Residente'}
            </Typography>
          </Box>
        </Box>
      </Box>

      <Divider />

      {/* Menú principal */}
      <List>
        {filteredMainItems.map((item) => (
          <ListItemButton
            key={item.path}
            selected={isActive(item.path)}
            onClick={() => handleMenuClick(item.path)}
            sx={{ mx: 1, borderRadius: 1 }}
          >
            <ListItemIcon sx={{ color: isActive(item.path) ? 'primary.main' : 'inherit' }}>
              {item.icon}
            </ListItemIcon>
            <ListItemText primary={item.label} />
          </ListItemButton>
        ))}
      </List>

      <Divider sx={{ my: 1 }} />

      {/* Menú de módulos */}
      <List>
        {filteredModuleItems.map((item) => (
          <React.Fragment key={item.key}>
            <ListItemButton
              onClick={() => handleExpandClick(item.key)}
              sx={{ mx: 1, borderRadius: 1 }}
            >
              <ListItemIcon sx={{ color: isActive(item.path) ? 'primary.main' : 'inherit' }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.label} />
              {expandedMenus[item.key] ? <ExpandLess /> : <ExpandMore />}
            </ListItemButton>
            
            <Collapse in={expandedMenus[item.key]} timeout="auto" unmountOnExit>
              <List component="div" disablePadding>
                {item.subItems.map((subItem) => (
                  <ListItemButton
                    key={subItem.path}
                    selected={isActive(subItem.path)}
                    onClick={() => handleMenuClick(subItem.path)}
                    sx={{ pl: 4, mx: 1, borderRadius: 1 }}
                  >
                    <ListItemIcon sx={{ 
                      minWidth: 36,
                      color: isActive(subItem.path) ? 'primary.main' : 'inherit' 
                    }}>
                      {subItem.icon}
                    </ListItemIcon>
                    <ListItemText 
                      primary={subItem.label}
                      primaryTypographyProps={{ variant: 'body2' }}
                    />
                  </ListItemButton>
                ))}
              </List>
            </Collapse>
          </React.Fragment>
        ))}
      </List>
    </Box>
  );

  return (
    <Drawer
      variant={variant}
      anchor="left"
      open={open}
      onClose={onClose}
      sx={{
        width: DRAWER_WIDTH,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: DRAWER_WIDTH,
          boxSizing: 'border-box',
          borderRight: '1px solid',
          borderColor: 'divider',
        },
      }}
    >
      {drawerContent}
    </Drawer>
  );
};

export default Sidebar;