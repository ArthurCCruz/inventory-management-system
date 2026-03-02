import { Button as MantineButton, ButtonProps as MantineButtonProps, MantineStyleProps } from "@mantine/core";
import { FC } from "react";
import { colors, borderRadius, shadows, animation } from "@/styles/theme";

export type ButtonVariant = 'primary' | 'secondary' | 'outlined' | 'danger';

interface CustomButtonProps extends Omit<MantineButtonProps, 'variant'>, MantineStyleProps {
  variant?: ButtonVariant;
  onClick?: () => void;
  component?: FC<any>;
  to?: string;
  type?: 'button' | 'submit' | 'reset';
}

const Button: FC<CustomButtonProps> = ({ 
  variant = 'primary', 
  children,
  style,
  ...props 
}) => {
  const getButtonStyles = () => {
    const baseStyles = {
      borderRadius: borderRadius.md,
      fontWeight: 600,
      transition: `all ${animation.normal} ease`,
      border: 'none',
    };

    switch (variant) {
      case 'primary':
        return {
          ...baseStyles,
          background: colors.primary.main,
          color: colors.text.white,
          '&:hover': {
            background: colors.primary.dark,
          },
        };
      case 'secondary':
        return {
          ...baseStyles,
          background: colors.background.light,
          color: colors.text.primary,
          border: `1px solid ${colors.border.light}`,
        };
      case 'outlined':
        return {
          ...baseStyles,
          background: 'transparent',
          color: colors.primary.main,
          border: `1.5px solid ${colors.primary.main}`,
        };
      case 'danger':
        return {
          ...baseStyles,
          background: '#ef4444',
          color: colors.text.white,
        };
      default:
        return baseStyles;
    }
  };

  const buttonStyles = getButtonStyles();

  return (
    <MantineButton
      {...props}
      style={{
        ...buttonStyles,
        ...style,
      }}
      styles={{
        root: {
          '&:hover': {
            transform: 'scale(1.02)',
            boxShadow: variant === 'primary' ? shadows.green : shadows.md,
          },
        },
      }}
      onMouseEnter={(e: React.MouseEvent<HTMLButtonElement>) => {
        e.currentTarget.style.transform = 'scale(1.02)';
        e.currentTarget.style.boxShadow = variant === 'primary' ? shadows.green : shadows.md;
      }}
      onMouseLeave={(e: React.MouseEvent<HTMLButtonElement>) => {
        e.currentTarget.style.transform = 'scale(1)';
        e.currentTarget.style.boxShadow = 'none';
      }}
    >
      {children}
    </MantineButton>
  );
};

export default Button;
