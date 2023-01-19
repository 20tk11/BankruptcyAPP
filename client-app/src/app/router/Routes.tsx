import { createBrowserRouter, RouteObject } from "react-router-dom";
import App from "../../App";
import CreateModel from "../../layouts/views/CreateModel";
import DocumentationPage from "../../layouts/views/DocumentationPage";
import HomePage from "../../layouts/views/HomePage";

export const routes: RouteObject[] = [
    {
        path: '/',
        element: <App />,
        children: [
            { path: '', element: <HomePage /> },
            { path: 'model', element: <CreateModel /> },
            { path: 'documentation', element: <DocumentationPage /> },
        ]
    }
]


export const router = createBrowserRouter(routes);