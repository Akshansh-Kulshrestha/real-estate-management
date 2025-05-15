# Real Estate Management System

A Django-based platform for managing properties, users, billing, maintenance, and more.

## Features
- Role-based login
- Property listings
- Invoices and payments
- Maintenance requests
- Admin dashboards
- REST APIs + Swagger

Core Models

1.	User: Extends Django's AbstractUser to include roles like agent, buyer, or admin.
2.	AgentProfile: Stores additional details specific to agents, such as agency affiliation and license number.
3.	BuyerProfile: Contains buyer-specific information like preferences and saved searches.
4.	Property: Represents individual property listings with details like title, description, price, and status.
5.	PropertyType: Categorizes properties (e.g., apartment, villa, studio).
6.	Location: Details about the property's geographical location, including city and area.
7.	Amenity: Lists available amenities (e.g., pool, gym) that can be associated with properties.
8.	PropertyImage: Handles multiple images per property listing 
9.	Enquiry: Tracks inquiries made by buyers regarding specific properties.
10.	Bookmark: Allows buyers to save properties for future reference 
________________________________________
Transaction & Booking Models
11.	Booking: Manages property viewing appointments between buyers and agents.
12.	Offer: Records offers made by buyers on properties, including status and timestamps.
##. Loan: Get loan easily 
13.	Transaction: Logs completed transactions, capturing details like amount and payment method.(Capterra)
14.	LeaseAgreement: Stores lease details for rented properties, including terms and duration.
________________________________________
Maintenance & Support Models
15.	MaintenanceRequest: Allows tenants to report issues requiring attention.(GitHub)
16.	MaintenanceLog: Tracks the progress and resolution of maintenance requests.(Chartered Institute of Housing (CIH))
17.	ServiceProvider: Information about third-party service providers for property maintenance.
________________________________________
Analytics & Reporting Models
18.	PropertyView: Logs each time a property listing is viewed, aiding in analytics.
19.	SearchQuery: Stores search queries made by users to analyze search patterns.(The CFO Club)
20.	Feedback: Collects user feedback on properties or the platform itself.
________________________________________
Security & Verification Models
21.	Document: Handles uploading and verification of documents related to properties or users.(The CFO Club)
22.	Verification: Manages verification processes for users and properties.
________________________________________
Billing & Payment Models
23.	Invoice: Generates invoices for transactions, including details like amount and due date.
24.	Payment: Records payments made, linked to invoices and transactions.
________________________________________
Content & Communication Models
25.	BlogPost: Manages blog content for the platform, including title, content, and publication date.
26.	Notification: Handles sending notifications to users about various events.
27.	Message: Facilitates direct messaging between users within the platform.

--------------------------------------
HTML FILES

Core Models (templates/core/)

* `user_profile.html`
* `edit_profile.html`
* `agent_dashboard.html`
* `buyer_dashboard.html`
* `property_list.html`
* `property_detail.html`
* `add_property.html`
* `edit_property.html`
* `property_type_list.html`
* `location_list.html`
* `amenity_list.html`
* `property_image_gallery.html`
* `enquiry_list.html`
* `enquiry_detail.html`
* `bookmarks.html`

---

Transaction & Booking (templates/booking/)

* `booking_list.html`
* `booking_detail.html`
* `make_booking.html`
* `offer_list.html`
* `make_offer.html`
* `transaction_list.html`
* `transaction_detail.html`
* `lease_agreement_list.html`
* `lease_agreement_detail.html`
* `apply_loan.html`
* `loan_status.html`

---

Maintenance & Support (templates/maintenance/)

* `maintenance_request_list.html`
* `maintenance_request_detail.html`
* `create_maintenance_request.html`
* `maintenance_logs.html`
* `service_provider_list.html`

---

Analytics & Reporting (templates/analytics/)

* `property_views.html`
* `search_query_log.html`
* `feedback_list.html`
* `submit_feedback.html`

---

Security & Verification (templates/verification/)

* `upload_document.html`
* `user_documents.html`
* `verify_document.html`
* `request_verification.html`
* `verify_verification.html`
* `pending_verifications.html`

---

Billing & Payment (templates/billing/)

* `invoice_list.html`
* `invoice_detail.html`
* `payment_list.html`
* `make_payment.html`
* `payment_success.html`

---

Content & Communication (templates/content/)

* `blog_list.html`
* `blog_detail.html`
* `create_blog_post.html`
* `notifications.html`
* `message_inbox.html`
* `message_detail.html`
* `send_message.html`

---

Shared / Base Templates (templates/includes/ or templates/base/)

* `base.html`
* `navbar.html`
* `footer.html`
* `login.html`
* `register.html`
* `dashboard.html`
* `403.html`
* `404.html`
* `500.html`




