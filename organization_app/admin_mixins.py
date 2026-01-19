class OrgBranchAdminMixin:
    """
    Restrict Django Admin data by organization & branch
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Superuser → full access
        if request.user.is_superuser:
            return qs

        # Safety: if user has no org, show nothing
        if not request.user.organization:
            return qs.none()

        # Organization Admin → all branches
        if (
            hasattr(request.user, "staff_role")
            and request.user.staff_role.role.name == "Organization Admin"
        ):
            return qs.filter(organization=request.user.organization)

        # Branch-level users
        return qs.filter(
            organization=request.user.organization,
            branch=request.user.branch
        )
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:

            if db_field.name == "organization":
                kwargs["queryset"] = Organization.objects.filter(
                    id=request.user.organization_id
                )

            if db_field.name == "branch":
                kwargs["queryset"] = Branch.objects.filter(
                    id=request.user.branch_id
                )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        # Creating new object
        if not change:
            obj.organization = request.user.organization
            obj.branch = request.user.branch

        super().save_model(request, obj, form, change)
