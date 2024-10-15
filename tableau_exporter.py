import os
import tableauserverclient as TSC
from config import SERVER_URL, TOKEN_NAME, PERSONAL_ACCESS_TOKEN, SITE_NAME, PROJECT_NAME, WORKBOOK_NAME, VIEW_NAME, FILTER_FIELD, ORIENTATION, OUTPUT_DIR, FILTER_VALUES
from utils import sanitize_filename

class TableauExporter:
    def __init__(self):
        self.server_url = SERVER_URL
        self.token_name = TOKEN_NAME
        self.personal_access_token = PERSONAL_ACCESS_TOKEN
        self.site_name = SITE_NAME
        self.tableau_auth = TSC.PersonalAccessTokenAuth(self.token_name, self.personal_access_token, self.site_name)
        self.server = TSC.Server(self.server_url, use_server_version=True)

    def sign_in(self):
        """Sign in to Tableau Server."""
        try:
            self.server.auth.sign_in(self.tableau_auth)
            print("Successfully signed in to Tableau Server")
        except TSC.ServerResponseError as e:
            print(f"Failed to sign in: {e}")
            raise

    def sign_out(self):
        """Sign out of Tableau Server."""
        self.server.auth.sign_out()

    def get_project(self, project_name):
        """Retrieve a project by name."""
        all_projects, _ = self.server.projects.get()
        return next((p for p in all_projects if p.name == project_name), None)

    def get_workbook(self, project_id, workbook_name):
        """Retrieve a workbook by name within a project."""
        # Initialize an empty list to store the workbooks from the specified project
        project_workbooks = []
        page_number = 1

        while True:
            # Set request options for the current page number
            wb_req_options = TSC.RequestOptions(pagenumber=page_number)
            workbooks, pagination_item = self.server.workbooks.get(req_options=wb_req_options)
            
            # Filter workbooks by project ID
            project_workbooks.extend([wb for wb in workbooks if wb.project_id == project_id])
            
            # Check if there are more pages to fetch
            if pagination_item.total_available <= pagination_item.page_number * pagination_item.page_size:
                break  # Stop if there are no more pages to fetch
            
            page_number += 1

        # Return the workbook that matches the given name
        return next((wb for wb in project_workbooks if wb.name == workbook_name), None)


    def get_dashboard_view(self, workbook, view_name):
        """Retrieve a view by name within a workbook."""
        self.server.workbooks.populate_views(workbook)
        return next((view for view in workbook.views if view.name == view_name), None)

    def export_pdf(self, dashboard_view, filter_values):
        """Export the view as PDF with specified filters."""
        for value in filter_values:
            filter_dict = {FILTER_FIELD: value}
            pdf_request_options = TSC.PDFRequestOptions(maxage=1, orientation=TSC.PDFRequestOptions.Orientation.Landscape)
            pdf_request_options.vf(FILTER_FIELD, value)

            # Generate sanitized filename
            sanitized_value = sanitize_filename(value)
            pdf_file_path = os.path.join(OUTPUT_DIR, f"{sanitized_value}.pdf")

            # Export and save the PDF
            with open(pdf_file_path, 'wb') as f:
                self.server.views.populate_pdf(dashboard_view, pdf_request_options)
                f.write(dashboard_view.pdf)

            print(f"Exported: {pdf_file_path}")

    def run(self):
        """Run the entire Tableau export process."""
        try:
            self.sign_in()

            project = self.get_project(PROJECT_NAME)
            if not project:
                print(f"Project '{PROJECT_NAME}' not found")
                return

            workbook = self.get_workbook(project.id, WORKBOOK_NAME)
            if not workbook:
                print(f"Workbook '{WORKBOOK_NAME}' not found in project '{PROJECT_NAME}'")
                return

            dashboard_view = self.get_dashboard_view(workbook, VIEW_NAME)
            if not dashboard_view:
                print(f"View '{VIEW_NAME}' not found in workbook '{WORKBOOK_NAME}'")
                return

            self.export_pdf(dashboard_view, FILTER_VALUES)
            
        finally:
            self.sign_out()

if __name__ == "__main__":
    exporter = TableauExporter()
    exporter.run()
