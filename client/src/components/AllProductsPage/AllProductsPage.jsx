import React from 'react'
import './AllProductsPage.css'
import ProductCard from '../ProductCard/ProductCard'
import { Typography } from '@mui/material'
import { useSelector, useDispatch } from 'react-redux'
import { Button } from '@mui/material';
import { getRecommendedProduct } from "../../Actions/productActions"

import { useEffect } from "react"

import axios from "axios"

const AllProductsPage = () => {
    const { product } = useSelector((state) => state.recommended);
    const dispatch = useDispatch()
    let prods = [];
    let { loading, products } = useSelector(state => state.products)
    const { user } = useSelector(state => state.user);
    if (products) {
        prods = products;
    }
    const { products: allproduct } = useSelector((state) => state.products);
    // console.log(allproduct);   
    let sub_cat = [];
    let brand = [];
    let item_id = [];

    let response = null;
    const trainModel = async () => {
        if (allproduct) {
            allproduct.forEach((el) => {
                sub_cat.push(el.subCategory);
                brand.push(el.brand);
                item_id.push(el._id);
               
                }
            )
console.log(sub_cat);
            

            try {
                response = await axios.post("http://127.0.0.1:8000/train3", {
                    "sub_cat": sub_cat,
                    "brand": brand,
                    "item_id": item_id,
                    
                });
                console.log(response.data);


            } catch (error) {
                console.error("Error:", error);
            }
        }
    }
    let result = null;
    let user_visisted_items = []
    const predict = async () => {
        if (user) {
            user.visited_items.forEach((el) => {
                user_visisted_items.push(el);
            })
        }
        const idsInDoubleQuotes = user_visisted_items.map(id => `"${id}"`);
        const visited = `[${idsInDoubleQuotes.join(',')}]`;
        console.log(user_visisted_items);

        try {
            result = await axios.post("http://127.0.0.1:8000/predict1", {
                "user_id": user._id
            });
            console.log(result.data);
            if (result.data && result.data.recommended_items) {
                await dispatch(getRecommendedProduct(result.data.recommended_items));
            }
        } catch (error) {
            console.error("Error:", error);
        }
    }
   
    return prods.length > 0 ? (
        <div className="productPage">
            <Typography variant='h3'>Explore, Shop, Enjoy it All!</Typography>
            <div className='allProductsContainer'>
                <div className="categoriesContainer">
                    <div className="categories">
                        <Typography variant='h5'>Categories</Typography>
                    </div>

                </div>
                <div className="productsDisplay">
                    {prods.map((item, index) =>

                    (
                        <ProductCard
                            heading={item.name}
                            subheading={item.description}
                            img={item.image.url}
                            price={item.price}
                            url={item._id}
                        />

                    ))}
                </div>
            </div>
           
        </div>
    ) : null
}

export default AllProductsPage
