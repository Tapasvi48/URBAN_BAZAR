const {postProduct,getAllProducts,getProductById,purchaseProduct, incrementVisitCount, getHighRatedProducts, last } = require("../controllers/productController")
const {lastVisitedProduct}=require("../controllers/userController");
const express = require("express")
const router = express.Router();
const isAuthenticated = require("../middleware/auth")


router.post("/postProduct",isAuthenticated,postProduct)
router.get("/getAllProducts",getAllProducts)
router.get("/product/:id",getProductById);
router.route("/product/buy/:id").get(isAuthenticated,purchaseProduct)
router.post("/product/:id",incrementVisitCount);
router.get("/productLast/:id",last)
router.get("/topRated",getHighRatedProducts)



module.exports = router