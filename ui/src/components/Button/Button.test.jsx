import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Button, { BUTTON_TYPE, BUTTON_VARIANT } from './Button';

describe('Button', () => {
  it('renders with default props', () => {
    render(<Button>Click me</Button>);
    const button = screen.getByRole('button', { name: /click me/i });
    expect(button).toBeInTheDocument();
    expect(button).toHaveAttribute('type', 'button');
    expect(button.className).toContain('Button');
    expect(button.className).toContain('solid-primary');
  });

  it('renders with custom type and variant', () => {
    render(<Button type={BUTTON_TYPE.TRANSPARENT} variant={BUTTON_VARIANT.WARNING}>Warning</Button>);
    const button = screen.getByRole('button', { name: /warning/i });
    expect(button).toHaveAttribute('type', 'button');
    expect(button.className).toContain('Button');
    expect(button.className).toContain('transparent-warning');
  });

  it('applies custom className', () => {
    render(<Button className="custom-class">Custom</Button>);
    const button = screen.getByRole('button', { name: /custom/i });
    expect(button).toHaveAttribute('type', 'button');
    expect(button.className).toContain('Button');
    expect(button.className).toContain('solid-primary');
    expect(button.className).toContain('custom-class');
  });

  it('renders as submit button', () => {
    render(<Button buttonType="submit">Submit</Button>);
    const button = screen.getByRole('button', { name: /submit/i });
    expect(button).toHaveAttribute('type', 'submit');
    expect(button.className).toContain('Button');
    expect(button.className).toContain('solid-primary');
  });

  it('renders with danger variant', () => {
    render(<Button variant={BUTTON_VARIANT.DANGER}>Danger</Button>);
    const button = screen.getByRole('button', { name: /danger/i });
    expect(button).toHaveAttribute('type', 'button');
    expect(button.className).toContain('Button');
    expect(button.className).toContain('solid-danger');
  });

  it('passes additional props to button element', () => {
    render(<Button disabled>Disabled</Button>);
    const button = screen.getByRole('button', { name: /disabled/i });
    expect(button).toBeDisabled();
    expect(button).toHaveAttribute('type', 'button');
    expect(button.className).toContain('Button');
    expect(button.className).toContain('solid-primary');
  });
});
