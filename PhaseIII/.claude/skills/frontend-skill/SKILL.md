---
name: frontend-skill
description: Build pages, components, layouts, and styling for web applications. Use for multi-page applications, dashboards, and interactive interfaces.
---

# Frontend Skill

## Instructions

1. **Layout Structure**
   - Define page-level layouts (header, footer, main content)
   - Use responsive grid or flexbox for sections
   - Organize reusable components

2. **Components**
   - Build buttons, cards, forms, modals, and navigation
   - Keep components modular and reusable
   - Use props and state effectively

3. **Styling**
   - Apply modern CSS techniques or Tailwind CSS
   - Maintain consistent spacing, typography, and colors
   - Ensure accessibility (contrast, focus states, ARIA labels)

4. **Interaction & UX**
   - Handle user events (clicks, hovers, inputs)
   - Implement responsive behavior for mobile and desktop
   - Add subtle animations and transitions for better UX

## Best Practices
- Keep component names descriptive and consistent
- Reuse components to reduce duplication
- Mobile-first design approach
- Ensure cross-browser compatibility
- Maintain clean and readable CSS structure

## Example Structure
```jsx
<Layout>
  <Header />
  <main className="container mx-auto p-4">
    <Card title="Welcome">
      <p>This is an example component</p>
      <Button onClick={handleClick}>Click Me</Button>
    </Card>
  </main>
  <Footer />
</Layout>
